#!/usr/bin/env python3
"""Grant (or inspect) OAuth scopes on WSO2 APIM Publisher API operations.

Auth: DCR + password grant using env vars (default WSO2_PRD_USER / WSO2_PRD_PASS).
Target: Publisher REST API v4 on WSO2 API Manager 4.2.

Examples:
  # List operations + current scopes
  python3 scripts/apim_grant_scope.py --api CharismaHelios --list

  # Dry-run: add tester to ALL operations
  python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester --ops all

  # Dry-run: add tester to specific GraphQL fields / REST targets
  python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester \\
      --ops fund,funds,QUERY:instrument

  # Apply + create revision + deploy to gateway
  python3 scripts/apim_grant_scope.py --api CharismaHelios --scope tester --ops all \\
      --apply --deploy
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import ssl
from typing import Any


DEFAULT_BASE = "https://apig-am.charisma.tech"
PUBLISHER = "/api/am/publisher/v4"
TOKEN_SCOPES = " ".join(
    [
        "apim:api_view",
        "apim:api_create",
        "apim:api_publish",
        "apim:api_manage",
        "openid",
    ]
)


class ApimError(RuntimeError):
    pass


def _http(
    method: str,
    url: str,
    *,
    data: Any = None,
    headers: dict[str, str] | None = None,
    form: bool = False,
    timeout: int = 60,
) -> tuple[int, Any]:
    h = dict(headers or {})
    body: bytes | None = None
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            h.setdefault("Content-Type", "application/x-www-form-urlencoded")
        elif isinstance(data, (dict, list)):
            body = json.dumps(data).encode()
            h.setdefault("Content-Type", "application/json")
        elif isinstance(data, bytes):
            body = data
        else:
            body = str(data).encode()
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            raw = resp.read()
            if not raw:
                return resp.status, None
            try:
                return resp.status, json.loads(raw.decode())
            except json.JSONDecodeError:
                return resp.status, raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            parsed = json.loads(raw.decode()) if raw else None
        except json.JSONDecodeError:
            parsed = raw.decode("utf-8", "replace") if raw else None
        raise ApimError(f"{method} {url} -> HTTP {e.code}: {parsed}") from e


class PublisherClient:
    def __init__(self, base: str, username: str, password: str):
        self.base = base.rstrip("/")
        self.username = username
        self.password = password
        self.token: str | None = None

    def login(self) -> None:
        basic_user = base64.b64encode(
            f"{self.username}:{self.password}".encode()
        ).decode()
        status, dcr = _http(
            "POST",
            f"{self.base}/client-registration/v0.17/register",
            data={
                "clientName": "apim_grant_scope_script",
                "owner": self.username,
                "grantType": "password refresh_token",
                "saasApp": True,
            },
            headers={"Authorization": f"Basic {basic_user}"},
        )
        if status not in (200, 201) or not isinstance(dcr, dict):
            raise ApimError(f"DCR failed: {status} {dcr}")
        cid = dcr["clientId"]
        csec = dcr["clientSecret"]
        token_basic = base64.b64encode(f"{cid}:{csec}".encode()).decode()
        status, tok = _http(
            "POST",
            f"{self.base}/oauth2/token",
            data={
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
                "scope": TOKEN_SCOPES,
            },
            headers={"Authorization": f"Basic {token_basic}"},
            form=True,
        )
        if status != 200 or not isinstance(tok, dict) or "access_token" not in tok:
            raise ApimError(f"Token failed: {status} {tok}")
        self.token = tok["access_token"]

    def _auth(self) -> dict[str, str]:
        if not self.token:
            raise ApimError("Not logged in")
        return {"Authorization": f"Bearer {self.token}"}

    def find_api(self, name: str) -> dict[str, Any]:
        q = urllib.parse.quote(f"name:{name}")
        status, body = _http(
            "GET",
            f"{self.base}{PUBLISHER}/apis?limit=25&query={q}",
            headers=self._auth(),
        )
        items = (body or {}).get("list") or []
        exact = [a for a in items if a.get("name") == name]
        if not exact:
            raise ApimError(f"API not found: {name!r} (matches={len(items)})")
        if len(exact) > 1:
            # Prefer PUBLISHED
            published = [a for a in exact if a.get("lifeCycleStatus") == "PUBLISHED"]
            exact = published or exact
        return exact[0]

    def get_api(self, api_id: str) -> dict[str, Any]:
        _, body = _http(
            "GET",
            f"{self.base}{PUBLISHER}/apis/{api_id}",
            headers=self._auth(),
        )
        if not isinstance(body, dict):
            raise ApimError(f"Unexpected API payload: {body!r}")
        return body

    def list_shared_scopes(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        offset = 0
        limit = 100
        while True:
            _, body = _http(
                "GET",
                f"{self.base}{PUBLISHER}/scopes?limit={limit}&offset={offset}",
                headers=self._auth(),
            )
            items = (body or {}).get("list") or []
            if not items:
                break
            out.extend(items)
            if len(items) < limit:
                break
            offset += limit
            if offset > 10000:
                break
        return out

    def find_shared_scope(self, name: str) -> dict[str, Any] | None:
        for s in self.list_shared_scopes():
            if s.get("name") == name:
                return s
        return None

    def update_api(self, api_id: str, api: dict[str, Any]) -> dict[str, Any]:
        _, body = _http(
            "PUT",
            f"{self.base}{PUBLISHER}/apis/{api_id}",
            data=api,
            headers={**self._auth(), "Content-Type": "application/json"},
        )
        if not isinstance(body, dict):
            raise ApimError(f"Unexpected update response: {body!r}")
        return body

    def create_revision(self, api_id: str, description: str) -> dict[str, Any]:
        _, body = _http(
            "POST",
            f"{self.base}{PUBLISHER}/apis/{api_id}/revisions",
            data={"description": description},
            headers=self._auth(),
        )
        if not isinstance(body, dict):
            raise ApimError(f"Unexpected revision response: {body!r}")
        return body

    def list_revisions(self, api_id: str) -> list[dict[str, Any]]:
        _, body = _http(
            "GET",
            f"{self.base}{PUBLISHER}/apis/{api_id}/revisions",
            headers=self._auth(),
        )
        return (body or {}).get("list") or []

    def delete_revision(self, api_id: str, revision_id: str) -> None:
        _http(
            "DELETE",
            f"{self.base}{PUBLISHER}/apis/{api_id}/revisions/{revision_id}",
            headers=self._auth(),
        )

    def get_deployments(self, api_id: str) -> list[dict[str, Any]]:
        _, body = _http(
            "GET",
            f"{self.base}{PUBLISHER}/apis/{api_id}/deployments",
            headers=self._auth(),
        )
        if isinstance(body, list):
            return body
        return (body or {}).get("list") or []

    def deploy_revision(
        self, api_id: str, revision_id: str, deployments: list[dict[str, Any]]
    ) -> Any:
        _, body = _http(
            "POST",
            f"{self.base}{PUBLISHER}/apis/{api_id}/deploy-revision?revisionId={revision_id}",
            data=deployments,
            headers=self._auth(),
        )
        return body


def op_key(op: dict[str, Any]) -> str:
    return f"{(op.get('verb') or '').upper()}:{(op.get('target') or '')}"


def parse_ops_selector(raw: str) -> str | set[str]:
    """Return 'all' or a set of selectors.

    Selectors accepted:
      - all
      - target                 (matches any verb with that target)
      - VERB:target            (exact)
    """
    raw = (raw or "").strip()
    if not raw or raw.lower() == "all":
        return "all"
    selectors: set[str] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            verb, target = part.split(":", 1)
            selectors.add(f"{verb.strip().upper()}:{target.strip()}")
        else:
            selectors.add(part)
    if not selectors:
        raise ApimError("Empty --ops selector")
    return selectors


def op_matches(op: dict[str, Any], selectors: str | set[str]) -> bool:
    if selectors == "all":
        return True
    assert isinstance(selectors, set)
    key = op_key(op)
    target = op.get("target") or ""
    return key in selectors or target in selectors


def ensure_api_scope(api: dict[str, Any], scope_name: str, shared: dict[str, Any]) -> bool:
    """Ensure shared scope is attached at API level. Returns True if changed."""
    scopes = list(api.get("scopes") or [])
    for entry in scopes:
        sc = entry.get("scope") if isinstance(entry, dict) else None
        if isinstance(sc, dict) and sc.get("name") == scope_name:
            return False
        if isinstance(entry, dict) and entry.get("name") == scope_name:
            return False
    scopes.append(
        {
            "scope": {
                "id": shared.get("id"),
                "name": shared["name"],
                "displayName": shared.get("displayName") or shared["name"],
                "description": shared.get("description") or "",
                "bindings": shared.get("bindings") or [],
                "usageCount": None,
            },
            "shared": True,
        }
    )
    api["scopes"] = scopes
    return True


def grant_scope_on_ops(
    api: dict[str, Any],
    scope_name: str,
    selectors: str | set[str],
) -> list[dict[str, Any]]:
    """Add scope_name to matching operations. Mutates api. Returns change rows."""
    changes: list[dict[str, Any]] = []
    ops = api.get("operations") or []
    for op in ops:
        if not op_matches(op, selectors):
            continue
        current = list(op.get("scopes") or [])
        # normalize to list of strings
        names: list[str] = []
        for s in current:
            if isinstance(s, str):
                names.append(s)
            elif isinstance(s, dict):
                names.append(s.get("scope") or s.get("name") or str(s))
            else:
                names.append(str(s))
        if scope_name in names:
            changes.append(
                {
                    "op": op_key(op),
                    "before": names,
                    "after": names,
                    "changed": False,
                }
            )
            continue
        after = names + [scope_name]
        op["scopes"] = after
        changes.append(
            {
                "op": op_key(op),
                "before": names,
                "after": after,
                "changed": True,
            }
        )
    return changes


def print_ops(api: dict[str, Any]) -> None:
    print(f"API {api.get('name')} {api.get('version')} id={api.get('id')} status={api.get('lifeCycleStatus')}")
    api_scopes = []
    for entry in api.get("scopes") or []:
        sc = entry.get("scope") if isinstance(entry, dict) else None
        if isinstance(sc, dict):
            api_scopes.append(
                f"{sc.get('name')}(shared={entry.get('shared')}, bindings={sc.get('bindings')})"
            )
    print("API scopes:", ", ".join(api_scopes) or "(none)")
    print("Operations:")
    for op in api.get("operations") or []:
        print(f"  {op_key(op):40s}  scopes={op.get('scopes')}")


def build_deploy_payload(existing: list[dict[str, Any]], vhost: str | None) -> list[dict[str, Any]]:
    if existing:
        out = []
        for d in existing:
            out.append(
                {
                    "name": d.get("name") or "Default",
                    "vhost": vhost or d.get("vhost"),
                    "displayOnDevportal": d.get("displayOnDevportal", True),
                }
            )
        return out
    return [
        {
            "name": "Default",
            "vhost": vhost or "apig-gw.charisma.tech",
            "displayOnDevportal": True,
        }
    ]


def ensure_revision_capacity(client: PublisherClient, api_id: str, max_revisions: int = 5) -> None:
    revs = client.list_revisions(api_id)
    if len(revs) < max_revisions:
        return
    # Delete oldest revision with no deployments
    undeployed = [r for r in revs if not (r.get("deploymentInfo") or [])]
    undeployed.sort(key=lambda r: r.get("createdTime") or 0)
    if not undeployed:
        raise ApimError(
            f"At revision cap ({max_revisions}) and no undeployed revision to delete"
        )
    victim = undeployed[0]
    print(f"Deleting oldest undeployed revision {victim.get('displayName')} ({victim.get('id')})")
    client.delete_revision(api_id, victim["id"])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Add a shared OAuth scope to WSO2 APIM API operations"
    )
    p.add_argument("--base-url", default=os.environ.get("WSO2_PRD_BASE", DEFAULT_BASE))
    p.add_argument("--user-env", default="WSO2_PRD_USER")
    p.add_argument("--pass-env", default="WSO2_PRD_PASS")
    p.add_argument("--api", default="CharismaHelios", help="API name in Publisher")
    p.add_argument("--scope", default="tester", help="Shared scope name to grant")
    p.add_argument(
        "--ops",
        default="all",
        help="all | comma list of targets or VERB:target (default: all)",
    )
    p.add_argument("--list", action="store_true", help="Only list operations/scopes")
    p.add_argument(
        "--apply",
        action="store_true",
        help="Persist API update (default is dry-run)",
    )
    p.add_argument(
        "--deploy",
        action="store_true",
        help="After --apply: create revision and deploy to gateway",
    )
    p.add_argument(
        "--vhost",
        default=None,
        help="Gateway vhost for deploy (default: current deployment / apig-gw.charisma.tech)",
    )
    p.add_argument(
        "--revision-desc",
        default=None,
        help="Revision description (default auto)",
    )
    args = p.parse_args(argv)

    user = os.environ.get(args.user_env)
    password = os.environ.get(args.pass_env)
    if not user or not password:
        print(
            f"Missing credentials: set {args.user_env} and {args.pass_env}",
            file=sys.stderr,
        )
        return 2

    client = PublisherClient(args.base_url, user, password)
    print(f"Connecting to {args.base_url} as {user} ...")
    client.login()
    print("Auth OK")

    meta = client.find_api(args.api)
    api_id = meta["id"]
    api = client.get_api(api_id)

    if args.list:
        print_ops(api)
        return 0

    selectors = parse_ops_selector(args.ops)
    shared = client.find_shared_scope(args.scope)
    if not shared:
        print(f"Shared scope not found: {args.scope!r}", file=sys.stderr)
        print("Available names containing that text:", file=sys.stderr)
        for s in client.list_shared_scopes():
            if args.scope.lower() in (s.get("name") or "").lower():
                print(f"  - {s.get('name')}", file=sys.stderr)
        return 1

    api_scope_added = ensure_api_scope(api, args.scope, shared)
    changes = grant_scope_on_ops(api, args.scope, selectors)
    matched = changes
    changed = [c for c in changes if c["changed"]]
    if not matched:
        print("No operations matched --ops selector", file=sys.stderr)
        return 1

    print(f"API: {api.get('name')} ({api_id})")
    print(f"Scope: {args.scope} (shared id={shared.get('id')})")
    print(f"API-level scope attach: {'YES (new)' if api_scope_added else 'already present'}")
    print(f"Matched ops: {len(matched)}  will-change: {len(changed)}")
    for c in matched:
        flag = "UPDATE" if c["changed"] else "skip"
        print(f"  [{flag}] {c['op']}: {c['before']} -> {c['after']}")

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to persist.")
        if args.deploy:
            print("(Note: --deploy ignored without --apply)")
        return 0

    if not changed and not api_scope_added:
        print("Nothing to update.")
        return 0

    updated = client.update_api(api_id, api)
    print(f"API updated. lastUpdatedTime={updated.get('lastUpdatedTime')}")

    if args.deploy:
        ensure_revision_capacity(client, api_id)
        desc = args.revision_desc or f"Grant scope {args.scope} on ops via apim_grant_scope.py"
        rev = client.create_revision(api_id, desc)
        rev_id = rev["id"]
        print(f"Created revision {rev.get('displayName')} ({rev_id})")
        deployments = build_deploy_payload(client.get_deployments(api_id), args.vhost)
        result = client.deploy_revision(api_id, rev_id, deployments)
        print("Deploy result:", json.dumps(result, ensure_ascii=False)[:1000])
    else:
        print("Skipped deploy. Gateway still serves previous revision until --deploy.")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ApimError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
