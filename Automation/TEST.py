import socket
import ssl
import pprint
from typing import List, Dict

def try_reverse_dns(ip: str) -> List[str]:
    """socket.gethostbyaddr / PTR"""
    try:
        # gethostbyaddr returns (hostname, aliaslist, ipaddrlist)
        hostname = socket.gethostbyaddr(ip)[0]
        return [hostname] if hostname else []
    except Exception:
        return []

def try_ptr_via_dns(ip: str) -> List[str]:
    """Attempt RFC-style PTR lookup using dnspython if available, else fallback to gethostbyaddr.
    (If you want strict PTR via dns.resolver, install dnspython and replace this.)"""
    # Fallback to the same as gethostbyaddr for simplicity
    return try_reverse_dns(ip)

def try_http_request(ip: str, timeout=5) -> List[str]:
    """Make an HTTP request to the IP and look for redirects or Host header echoes."""
    import http.client
    candidates = []
    try:
        conn = http.client.HTTPConnection(ip, timeout=timeout)
        conn.request("GET", "/", headers={"User-Agent": "curl/7.0"})
        resp = conn.getresponse()
        # Look for Location header (redirect)
        loc = resp.getheader("Location")
        if loc:
            candidates.append(loc)
        # Some servers echo canonical hostname in headers or body; check Server header
        srv = resp.getheader("Server")
        if srv:
            candidates.append(srv)
        conn.close()
    except Exception:
        pass
    return candidates

def try_https_cert(ip: str, timeout=5) -> List[str]:
    """Connect to ip:443 and fetch presented certificate (may be default cert).
       Parse CN and SAN entries. This does not require correct SNI but servers may present a default cert."""
    candidates = []
    ctx = ssl.create_default_context()
    # We set server_hostname to the IP so SNI is the IP — server may present default certificate.
    try:
        with socket.create_connection((ip, 443), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                # cert is a dict; get subjectAltName and commonName
                san = cert.get('subjectAltName', ())
                for t, name in san:
                    if t.lower() in ('dns',):
                        candidates.append(name)
                # get CN from subject
                subject = cert.get('subject', ())
                for s in subject:
                    for k, v in s:
                        if k == 'commonName':
                            candidates.append(v)
    except Exception:
        pass
    return candidates

def resolve_ip_to_host_candidates(ip: str) -> Dict[str, List[str]]:
    results = {}
    results['reverse_dns_gethostbyaddr'] = try_reverse_dns(ip)
    results['ptr_dns'] = try_ptr_via_dns(ip)
    results['http_try'] = try_http_request(ip)
    results['https_cert'] = try_https_cert(ip)
    # Deduplicate and return
    for k in results:
        # Normalize simple things (strip trailing dots)
        results[k] = list(dict.fromkeys([r.rstrip('.') for r in results[k]]))
    return results

if __name__ == "__main__":
    ip = "209.236.103.90"   # replace with the IP you're investigating
    pprint.pprint(resolve_ip_to_host_candidates(ip))
