# Bismillah.

# Cybersecurity — Core-Complete Viva Recall

> **Source boundary:** there is no standalone cybersecurity slide folder in this workspace. This is a rigorous standard-core supplement built around the reported BRAC viva questions, the security material in your networking/OOP/SWE background, and the concepts required to defend your Matter thesis. It is not labeled as a local-slide transcription.

Security answers should begin with the asset, adversary, and threat model. “Use encryption” is incomplete until you say **what is encrypted, against whom, where the key lives, and what integrity/authentication mechanism is used**.

---

# 1. Security objectives and vocabulary

## 1.1 CIA triad

- **Confidentiality:** unauthorized parties cannot learn protected information. Controls include access control, encryption, segmentation, minimization, and secure deletion.
- **Integrity:** unauthorized or accidental modification is prevented or detectable. Controls include authenticated encryption, MACs, digital signatures, validation, database constraints, versioning, and audit logs.
- **Availability:** authorized users can access the service/data when needed. Controls include redundancy, backups, capacity planning, rate limiting, failover, monitoring, and denial-of-service resistance.

One control can affect several goals. Encryption supports confidentiality, but encryption without authentication may not protect integrity. Backups support availability, but an unencrypted backup can violate confidentiality.

### Exact viva answer

> “The CIA triad is confidentiality, integrity, and availability. Confidentiality restricts disclosure, integrity prevents or detects unauthorized modification, and availability keeps systems usable for authorized users. A secure design balances all three according to its threat model.”

## 1.2 Additional properties

- **Authentication:** establish an identity or the origin of data.
- **Authorization:** decide what an authenticated principal may do.
- **Accountability/auditing:** actions can be associated with principals through trustworthy records.
- **Non-repudiation:** evidence makes it difficult for a signer to credibly deny a signed action; this requires more than an ordinary application log.
- **Privacy:** appropriate collection, use, retention, and disclosure of personal data; it is broader than secrecy.
- **Safety:** prevent unacceptable physical/human harm. A system can be secure against an attacker yet unsafe due to a design error.

## 1.3 Threat, vulnerability, exploit, and risk

- **Asset:** something of value—credentials, money, health data, availability, reputation, device control.
- **Threat:** a possible cause of harm.
- **Threat actor/adversary:** entity with capabilities and goals.
- **Vulnerability:** a weakness that can be used or triggered.
- **Exploit:** technique/input that takes advantage of a vulnerability.
- **Risk:** expected harm, often ranked qualitatively as likelihood × impact.
- **Control/mitigation:** measure that prevents, detects, limits, or helps recover from harm.
- **Residual risk:** risk remaining after controls.

Do not call every bug a vulnerability. A vulnerability needs a plausible security consequence under stated assumptions.

---

# 2. Security design principles

## 2.1 Least privilege

Give each user, process, service, and key only the permissions needed for the required duration. Separate read, write, administration, deployment, and key-management roles. Remove stale accounts and privileges.

## 2.2 Defense in depth

Use independent layers so one failure is not catastrophic: authenticated user → object-level authorization → service identity → network policy → database role → encryption → detection/audit. Layers should address different failure modes; repeating the same weak check is not depth.

## 2.3 Fail securely

When validation, authorization, dependency, or policy lookup fails, default to the safe state. “Fail closed” does not mean crash the whole service; design an explicit safe degradation path.

## 2.4 Complete mediation

Check authorization on every protected operation and object, not only when the user opens a page. A hidden button is not an authorization control.

## 2.5 Separation of duties

Split dangerous powers. For example, the person who requests a high-value payment should not be the only person who approves it; an application service should not also control the master encryption key without a justified boundary.

## 2.6 Minimize attack surface and data

Disable unused services/endpoints, validate exposed interfaces, collect only necessary data, retain it only as long as required, and keep secrets out of clients/logs/source control.

## 2.7 Never trust the client

The client is under user control. Recalculate prices, roles, ownership, and state transitions on the server. Validate but do not rely on UI restrictions, hidden fields, or client-side checks.

---

# 3. Threat modeling

## 3.1 Five questions

1. What are we building—components, data flows, trust boundaries?
2. What assets and security properties matter?
3. Who is the adversary and what can they access/control?
4. What can go wrong?
5. Which preventive, detective, and recovery controls reduce risk, and how will we verify them?

## 3.2 STRIDE recall

| Category | Violated idea | Example | Typical controls |
|---|---|---|---|
| Spoofing | authentication | stolen session token | MFA, secure session handling |
| Tampering | integrity | modified API request/state | authorization, MAC/signature, validation |
| Repudiation | accountability | denying an administrative action | protected audit trails, signatures where needed |
| Information disclosure | confidentiality | secret in log/backup | minimization, access control, encryption |
| Denial of service | availability | request/resource exhaustion | quotas, rate limits, isolation, capacity |
| Elevation of privilege | authorization | ordinary user becomes admin | least privilege, server-side policy checks |

STRIDE is a prompt for analysis, not proof that every threat was found.

## 3.3 Attack trees

Write the attacker’s goal at the root, decompose into OR alternatives and AND prerequisites, then attach controls/cost/evidence. Attack trees are especially useful when a single goal can be achieved through credentials, implementation bugs, social engineering, or physical access.

---

# 4. Cryptographic primitives

## 4.1 Symmetric encryption

The same secret key encrypts/decrypts. It is fast and used for bulk data. Examples: AES and ChaCha20.

Encryption must use a secure construction/mode. **AEAD**—such as AES-GCM or ChaCha20-Poly1305—provides confidentiality and integrity/authenticity together.

Conceptually:

```text
(ciphertext, tag) = AEAD_Encrypt(key, nonce, plaintext, associated_data)
plaintext         = AEAD_Decrypt(key, nonce, ciphertext, tag, associated_data)
```

Associated data is authenticated but not encrypted—for example, a protocol version or record identifier.

### Nonce rule

Many AEAD schemes require a nonce that is unique for each encryption under the same key. Reusing an AES-GCM or stream-cipher nonce can reveal relationships between plaintexts and break authentication. A nonce need not be secret; it must follow the construction’s uniqueness/randomness requirement.

Never use ECB for structured data: identical plaintext blocks produce identical ciphertext blocks. CBC/CTR alone do not authenticate ciphertext; pair them correctly with a MAC or use AEAD.

## 4.2 Asymmetric cryptography

A public/private key pair supports operations such as encryption/key encapsulation, signature, or key agreement, depending on the scheme.

- Public-key operations are slower than symmetric bulk encryption.
- Hybrid protocols use public-key methods to authenticate/establish a session secret, then symmetric AEAD for application data.
- RSA, elliptic-curve signatures, and Diffie–Hellman solve different jobs; “asymmetric encryption” is not one universal operation.

## 4.3 Key agreement and forward secrecy

Diffie–Hellman lets parties derive a shared secret over an insecure channel, but unauthenticated DH is vulnerable to man-in-the-middle attack. Authenticate the exchange with certificates/signatures or a pre-established method.

Ephemeral DH keys give **forward secrecy**: later compromise of the server’s long-term signing key does not by itself decrypt previously recorded sessions, assuming ephemeral secrets were erased and the protocol was correctly used.

## 4.4 Hash functions

A cryptographic hash maps arbitrary input to fixed-length output. Desired properties include:

- preimage resistance: hard to find an input matching a given digest;
- second-preimage resistance: given one input, hard to find a different one with the same digest;
- collision resistance: hard to find any two distinct inputs with the same digest.

Collisions are mathematically unavoidable because the input space is larger than the output space. For an ideal `n`-bit hash, a generic collision search needs roughly `2^(n/2)` work due to the birthday effect, not `2^n`.

A bare hash does not authenticate a message: an attacker who can change the message can calculate a new public hash.

## 4.5 MAC and HMAC

A message authentication code uses a shared secret to authenticate message integrity/origin. HMAC is a secure construction built around a cryptographic hash. Both sender and verifier know the key, so a MAC does not provide public non-repudiation.

## 4.6 Digital signatures

The signer uses a private key; anyone with the public key can verify. A signature gives integrity and origin authentication under key-management assumptions. Sign the intended structured representation/domain, not an ambiguous string. Verification also needs certificate/key trust, revocation/expiry policy, and replay context.

## 4.7 Encoding is not encryption

- Base64/hex: reversible representation with no secret.
- Encryption: confidentiality using a key.
- Hashing: one-way digest; no decryption operation.
- Compression: redundancy reduction; not secrecy.

---

# 5. Password storage

## 5.1 Correct answer

> “Passwords should normally be stored using a per-password random salt and a deliberately slow password KDF such as Argon2id, scrypt, bcrypt, or appropriately configured PBKDF2—not reversible encryption and not a fast general hash. On login, derive again with the stored salt and parameters and compare in constant-time where supported.”

Record format conceptually stores:

```text
algorithm | parameters | salt | derived_hash
```

- **Salt:** unique random value; prevents identical passwords sharing a digest and defeats one precomputed table across all users. It is stored openly.
- **Work factor/memory cost:** makes each guess expensive; parameters should be upgradeable.
- **Pepper:** optional application-wide secret kept separately in a secret manager/HSM. It does not replace salt and complicates rotation/recovery.

Rate limiting and MFA help against online guessing; a slow KDF mainly limits offline guessing after database theft. Reset tokens should be random, short-lived, single-use, and preferably stored hashed.

## 5.2 Why plain SHA-256 is wrong for passwords

SHA-256 is designed to be fast. Attackers with GPUs can test enormous dictionaries quickly. Adding a salt stops precomputation/reuse but does not make each guess expensive enough; the password KDF supplies tunable CPU/memory cost.

---

# 6. How to ensure confidentiality of files on your system

## 6.1 Complete viva answer

> “First I define the threat: a stolen disk, another local user, malware running under my account, a privileged administrator, or a leaked backup require different controls. I restrict access with least-privilege OS permissions, encrypt data at rest with full-disk or file-level encryption, protect data in transit with authenticated protocols, and keep keys outside the encrypted data with secure backup and rotation. I also encrypt backups, avoid secrets in logs/temp files, patch the system, lock the session, and audit access. Encryption at rest protects a powered-off stolen disk, but it does not protect a file after malware has obtained my unlocked session and key access.”

## 6.2 Full-disk versus file/application encryption

| Control | Strong against | Important limitation |
|---|---|---|
| Full-disk encryption | lost/stolen powered-off storage | transparent after login/unlock |
| Filesystem/file encryption | selected paths and sometimes user separation | keys often available during active session |
| Application/field encryption | database/storage admins or narrower trust boundary, depending on key placement | search/indexing and key-service complexity |
| Permissions/ACLs | other users/processes under OS policy | privileged compromise/misconfiguration may bypass |
| Encrypted backup | lost/leaked backup media | key loss makes recovery impossible |

## 6.3 Key management

Key management often dominates the security of encryption:

- generate keys with a cryptographically secure random generator;
- store them in OS keystore, secret manager, KMS, TPM/HSM as appropriate;
- separate data and keys;
- restrict use, not merely key-file read access;
- rotate/version keys and plan re-encryption;
- back up recovery keys securely;
- log key use without logging the key;
- revoke on compromise;
- securely erase plaintext/temp files where the storage threat model makes that meaningful.

Hard-coding a key in source, mobile app, environment dump, or the same database does not create a useful security boundary.

---

# 7. Should database entries be encrypted?

## 7.1 Strong answer

> “Encrypt sensitive data according to its classification and threat model, not every field blindly. Use TLS for data in transit and disk/TDE for stolen-media protection. For highly sensitive fields, use application- or column-level authenticated encryption with keys in a separate KMS and strict access/auditing. Field encryption can break indexing, sorting, range queries, constraints, analytics, and key rotation, so non-sensitive fields may rely on access control and storage encryption. Passwords are the special case: store salted slow hashes, not decryptable ciphertext.”

## 7.2 Layers and the threats they address

- **TLS connection:** protects client/server traffic from network interception/tampering.
- **Disk/storage encryption:** protects lost media/snapshots; a running DB with keys can still read data.
- **Transparent Database Encryption (TDE):** encrypts database files/logs/backups beneath queries; a compromised DB account still sees plaintext.
- **Column/database-function encryption:** narrows exposure but DB may still hold/use keys.
- **Application-level encryption:** DB sees ciphertext; strongest separation from DB administrators if keys are elsewhere, but query capability becomes limited.
- **Tokenization:** replace sensitive value with a token and keep mapping in a separate protected service.

## 7.3 Queryability trade-offs

Randomized authenticated encryption hides equality patterns but ordinary equality/range indexes stop working. Deterministic encryption can support equality lookup but reveals repeated values and frequency patterns. Order-preserving approaches leak even more. Do not choose searchable encryption casually; state the leakage and business need.

## 7.4 Data lifecycle

Classification, retention, backups, replicas, exports, caches, logs, analytics warehouses, and deletion matter as much as the primary table. Encrypting one column while copying plaintext to logs or CSV exports defeats the control.

---

# 8. Authentication, authorization, and access control

## 8.1 Authentication versus authorization

- Authentication: “Who are you?”
- Authorization: “May this principal perform this action on this object now?”

A valid login does not authorize access to every object. Enforce policy server-side at the object/action boundary.

## 8.2 Authentication factors

- knowledge: password/PIN;
- possession: authenticator/device/hardware key;
- inherence: biometric.

Two passwords are not two-factor. MFA uses independent factor types. Biometrics are probabilistic and difficult to revoke, so they normally unlock a protected credential rather than replace all key material.

## 8.3 Session cookies

Use an unpredictable session identifier; store session state server-side or use protected tokens. Cookies should commonly be `Secure`, `HttpOnly`, and appropriate `SameSite`; rotate the session identifier after authentication/privilege change, expire/revoke sessions, and protect state-changing requests against CSRF.

## 8.4 JWT

A JWT is a token format, not an authentication system by itself. Validate:

- expected signature algorithm—never accept attacker-selected `none`;
- signature with the correct key;
- issuer, audience, expiry/not-before;
- token type/purpose and required claims;
- authorization against current server policy.

Signed JWT content is readable unless separately encrypted. Short lifetime limits exposure; revocation/state changes are harder than with server sessions. Never put secrets in an ordinary signed JWT payload.

## 8.5 OAuth 2.0 and OpenID Connect

- OAuth 2.0 delegates authorization to access protected resources.
- OpenID Connect adds an identity/authentication layer and ID token.
- Authorization Code with PKCE protects modern public clients against code interception.

Validate redirect URIs exactly, state/nonce as applicable, issuer/audience/signatures, and token destination. “Login with Google” normally uses OIDC, not bare OAuth as an authentication proof.

## 8.6 RBAC and ABAC

- **RBAC:** permissions assigned through roles; simple and auditable but can cause role explosion.
- **ABAC:** policy uses subject, object, action, and environment attributes; expressive but harder to reason about/test.

Object ownership checks are still required: a role of `user` does not let one user read another user’s incident report.

---

# 9. TLS and HTTPS

## 9.1 What TLS provides

TLS protects application traffic with:

- confidentiality through symmetric encryption;
- integrity/authenticity through AEAD;
- server authentication through certificate validation;
- optional client authentication;
- forward secrecy in modern ephemeral-key handshakes.

HTTPS is HTTP carried over TLS.

## 9.2 High-level handshake

1. Client sends supported versions, cipher options/key share, randomness, and requested server name.
2. Server selects parameters, sends its key share and certificate chain, and proves possession of the certificate’s private key.
3. Client verifies hostname, validity, chain/trust, signature, and policy.
4. Both derive symmetric traffic keys from the authenticated key exchange.
5. Finished messages authenticate the transcript; application records then use AEAD.

TLS does not say the application is trustworthy, prevent an authorized server from leaking data, or fix SQL injection. If certificate verification is disabled, encryption may terminate at the attacker.

## 9.3 SYN/ACK versus TLS

The TCP three-way handshake (`SYN`, `SYN-ACK`, `ACK`) establishes transport state and sequence numbers. The TLS handshake then establishes authenticated cryptographic keys over that connection. TCP ACK means acknowledgment; it is not a cryptographic guarantee.

---

# 10. Network security controls

## 10.1 Firewall, WAF, IDS, and IPS

- Firewall filters network traffic by addresses, ports, state, and policy.
- WAF inspects HTTP/application patterns; it supplements secure code rather than fixing it.
- IDS detects suspicious activity and alerts.
- IPS sits inline and can block, creating false-positive/availability trade-offs.

## 10.2 Segmentation

Separate user, application, database, management, and sensitive workloads; allow only necessary flows. Segmentation limits lateral movement after one component is compromised.

## 10.3 VPN

A VPN creates an authenticated encrypted tunnel between endpoints/networks. It protects traffic on the path but does not make the endpoint or tunneled application safe. Broad VPN access can increase blast radius without internal authorization/segmentation.

## 10.4 NAT is not a firewall

NAT translates addresses/ports. Stateful NAT may incidentally block unsolicited inbound mappings, but security policy should be expressed by a firewall. IPv6’s large address space and lack of mandatory NAT do not mean hosts must be exposed.

## 10.5 DNS and email protections

DNSSEC authenticates DNS data origin/integrity; it does not encrypt queries. DoH/DoT encrypt resolver traffic but shift trust to the resolver. SPF, DKIM, and DMARC address different parts of sender authorization/message signing/domain policy and do not make every email trustworthy.

---

# 11. Web and API vulnerabilities

## 11.1 SQL injection

Cause: untrusted input changes SQL syntax.

Wrong:

```java
String sql = "SELECT * FROM users WHERE email='" + email + "'";
```

Correct pattern:

```java
PreparedStatement ps = connection.prepareStatement(
    "SELECT id, role FROM users WHERE email = ?"
);
ps.setString(1, email);
ResultSet rs = ps.executeQuery();
```

Parameterized queries separate code from data. Also use least-privilege DB accounts and allow-list identifiers when a value cannot be parameterized, such as a selected sort column.

## 11.2 Cross-site scripting (XSS)

Untrusted data becomes executable browser content. Prevent with context-aware output encoding, safe templating, sanitization when HTML is intentionally accepted, avoiding dangerous DOM sinks, and a restrictive Content Security Policy as defense in depth.

- stored XSS persists on server;
- reflected XSS returns attacker-controlled request data;
- DOM XSS occurs in client-side source/sink logic.

## 11.3 CSRF

The attacker causes a victim’s browser to send an unwanted state-changing request using automatically attached credentials. Use SameSite cookies, unpredictable CSRF tokens, Origin/Referer validation where appropriate, and re-authentication for high-risk actions. CSRF differs from XSS; XSS can often bypass CSRF defenses from within the trusted origin.

## 11.4 Broken object-level authorization / IDOR

Changing `/reports/123` to `/reports/124` reveals another user’s object because the server checked authentication but not ownership/policy. Query by both object ID and authorized principal or apply a centralized policy check on every operation.

## 11.5 SSRF

The server fetches an attacker-chosen URL, allowing access to internal services or cloud metadata. Use strict destination allow-lists, safe URL parsing/resolution, block private/link-local ranges after DNS resolution, control redirects, restrict egress, and isolate fetchers.

## 11.6 Command injection

Untrusted input enters a shell command. Prefer library APIs and fixed argument arrays; avoid a shell, allow-list choices, and run with least privilege. Escaping alone is fragile across shells/platforms.

## 11.7 Path traversal and file upload

Canonicalize and confine paths to an approved root; generate server-side filenames; validate type/content/size; store outside executable/web roots; scan when justified; set quotas; and serve with safe content disposition/type. Checking only the extension is insufficient.

## 11.8 CORS

CORS is a browser policy controlling which origins may read cross-origin responses. It is not authentication and does not stop direct requests from scripts outside the browser. Never combine credentialed access with an arbitrary reflected origin.

## 11.9 Rate limiting and abuse controls

Choose the identity and resource being protected—account, IP, device, API key, endpoint, expensive operation. Use quotas/token buckets, progressive delay, lockout carefully, bot detection where justified, and monitoring. A single global IP limit can punish users behind NAT and can be bypassed by distributed attackers.

---

# 12. Secure software lifecycle and operations

## 12.1 Shift left and keep runtime controls

Security requirements and threat modeling begin during design. Use code review, tests, static/dynamic analysis, dependency/secret/container scanning, and controlled CI/CD. Runtime still needs least privilege, monitoring, rate limits, incident response, and patching; testing cannot prove absence of vulnerabilities.

## 12.2 Secrets

Keep secrets out of repositories, mobile/web bundles, logs, images, and ordinary shared documents. Use a secret manager/KMS, short-lived credentials, workload identity where possible, scoped permissions, rotation, and emergency revocation. After a leak, removing the Git line is insufficient; revoke/rotate the credential and investigate access.

## 12.3 Logging

Log authentication, authorization denials, administrative actions, security-policy changes, critical state transitions, and correlation IDs. Protect integrity/access/retention. Do not log passwords, tokens, private keys, full payment data, or unnecessarily sensitive personal data.

## 12.4 Backups and ransomware

Use versioned/offline or immutable copies, separate credentials, encryption, monitored backup jobs, and regular restore tests. A backup that has never been restored is an assumption, not a recovery control.

## 12.5 Vulnerability handling

Confirm scope and reproducibility, assess impact/exploitability, contain, patch/mitigate, rotate exposed credentials, monitor for abuse, communicate appropriately, and perform root-cause/post-incident improvement. Preserve evidence and avoid silently destroying logs.

---

# 13. High-probability viva questions

## “How do you ensure confidentiality?”

> “Classify the data and define the attacker. Enforce least-privilege access, encrypt in transit and at rest with authenticated schemes, separate and protect keys, minimize collection/retention, secure backups/logs/temp copies, and audit access. Encryption is one layer; an authorized compromised endpoint can still read plaintext.”

## “Does hashing provide confidentiality?”

No. A hash is not encryption and has no decryption key. It supports fingerprinting/integrity constructions; low-entropy input such as passwords can still be guessed unless protected by a salted slow KDF.

## “Can encryption alone ensure integrity?”

Not ordinary unauthenticated encryption. Use AEAD or an encrypt-then-MAC construction correctly. Otherwise ciphertext may be malleable.

## “Why not encrypt every database column?”

Because protection should match sensitivity/threats, while field encryption adds key, index, query, constraint, analytics, rotation, and availability costs. Encrypt sensitive fields with the right boundary; use access control/TDE for other risks; hash passwords.

## “What if the encryption key is stored beside the data?”

It may still help against accidental media loss under some setups, but it gives little separation against compromise that reads both. Put keys in a separate controlled keystore/KMS/HSM boundary with scoped use and audit.

## “Authentication succeeded; why check authorization again?”

Authentication establishes identity, not permission for this action/object. Every protected operation needs current server-side authorization.

## “Can TLS stop phishing or malware?”

TLS authenticates the domain endpoint under PKI assumptions and protects transport. A malicious authenticated site can still phish, and malware on an endpoint can access data before encryption or after decryption.

## “Is perfect security possible?”

Not for a useful real system. Security manages risk under assumptions, costs, usability, and changing threats. State residual risk and verify controls continuously.

---

# 14. Final security self-test

- [ ] Define every CIA property with one control and one failure example.
- [ ] State an asset/adversary/trust boundary before proposing a defense.
- [ ] Distinguish encryption, hashing, MAC, signature, encoding, and key agreement.
- [ ] Explain AEAD and the nonce-reuse danger.
- [ ] Explain salted slow password hashing and why SHA-256 alone is inadequate.
- [ ] Give the full file-confidentiality answer and its unlocked-endpoint limitation.
- [ ] Give the layered database-encryption answer, including queryability and key management.
- [ ] Explain a modern TLS handshake at the certificate/key/session level.
- [ ] Separate authentication, authorization, session, JWT, OAuth, and OIDC.
- [ ] Defend SQLi, XSS, CSRF, IDOR, SSRF, command injection, traversal, upload, and CORS controls.
- [ ] Explain why NAT, TLS, a WAF, or encryption alone is never the complete security story.
