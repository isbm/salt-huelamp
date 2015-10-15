## Philips HUE Lamps Controller

This is a Philips lamp controller proxy minion with the caller module.
You can use it in "production" (at your home, e.g.) or for the demo purposes.

### Requirements

1. Salt Master running
2. Salt Proxy installed somewhere
3. Philips HUE lamps

### Setup Proxy Minion

On the Proxy Minion:

- Create the following file: `/etc/salt/proxy`

- Add there the followinf content:
```
   master: yourhost.domain.name
```

On the Master configure pillar (e.g. if your pillars are /srv/salt/pillar/...):

- In the `/srv/salt/pillar/top.sls`:
```
  base:
    'myminion':
       - myminion
```

- In the `/srv/salt/pillar/myminion.sls`:
```
  proxy:
    proxytype: philips_hue
    user: newdeveloper
    host: IP.ADDR.OF.THE.HUE.BRIDGE
```

After this:

1. Start Salt Master by `salt-master ...` on the Master machine.
2. Start Salt Proxy Minion by `salt-proxy ...` on the Proxy machine.
3. Call HUE lamps from the Salt Master: `salt myminion hue.status` for example.
