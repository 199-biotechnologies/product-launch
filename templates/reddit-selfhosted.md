# r/selfhosted — {{name}}

## Title

{{name}}: {{tagline}} (selfhosted alternative to [named SaaS])

## Body

**What it is:** {{tagline}}

**Selfhosted alternative to:** [named SaaS if applicable]

**Resource requirements:**
- RAM: [X MB/GB]
- Disk: [X MB/GB]
- CPU: [minimal/moderate/heavy]
- Network: [lan/wan/both]

**Deployment:**

```yaml
# docker-compose.yml
version: '3'
services:
  {{slug}}:
    image: [image]
    ports:
      - "[port]:[port]"
    volumes:
      - ./data:/data
    environment:
      - KEY=value
```

Or: [alternative install — systemd, binary, etc.]

**Backup story:**
[How do I back this up? Where does state live?]

**Auth:**
[How auth works. SSO? Local? None? Reverse proxy integration?]

**Repo:** {{url}}

**License:** [MIT/Apache/GPL/AGPL]

<!--
r/selfhosted requires Docker Compose + docs. Resource requirements + backup story earn trust.
Account 30+ days, 50+ karma.
-->
