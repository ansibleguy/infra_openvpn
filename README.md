# WORK-IN-PROGRESS! DON'T USE IN PRODUCTION!

<a href="https://openvpn.net/community/">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/OpenVPN_logo.svg/1280px-OpenVPN_logo.svg.png" alt="OpenVPN Logo" width="500"/>
</a>

# Ansible Role - OpenVPN Client-to-Site VPN

Role to deploy OpenVPN Client-to-Site VPN setups.

[![Molecule Test Status](https://badges.ansibleguy.net/infra_openvpn.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/infra_openvpn.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/infra_openvpn.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/infra_openvpn.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/ansibleguy/infra_openvpn)

[Molecule Logs (if failed)](https://badges.ansibleguy.net/log/molecule_infra_openvpn_test.log)

## OpenVPN Editions

This role uses the [OpenSource](https://github.com/OpenVPN/openvpn) [OpenVPN Community](https://openvpn.net/community/) edition.

**Why use the community edition?**

* Pros:
  * No license fees - one server can scale up to thousands of clients without any major costs
  * All major functionalities are covered by the opensource edition
  * Manageable using Ansible

* Cons
  * This edition has no graphical (_web-_) user-interface!
    
    If you are searching for a pretty web-ui to click at => check out the [OpenVPN Access Server](https://openvpn.net/access-server/)


**Tested:**
* Debian 11

## Install

```bash
# latest
ansible-galaxy role install git+https://github.com/ansibleguy/infra_openvpn

# from galaxy
ansible-galaxy install ansibleguy.infra_openvpn

# or to custom role-path
ansible-galaxy install ansibleguy.infra_openvpn --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)


* **Configuration**
  * 


  * **Default config**:
    * 
 

  * **Default opt-ins**:
    * 


  * **Default opt-outs**:
    * 

## Info

* **Info:** If you want to know more about configuring OpenVPN-community - check out their [comprehensive documentation](https://community.openvpn.net/openvpn/wiki)

  Interesting pages:

  * [Security overview](https://community.openvpn.net/openvpn/wiki/SecurityOverview)

  * [Hardening](https://openvpn.net/community-resources/hardening-openvpn-security/), [Hardening (older Version)](https://community.openvpn.net/openvpn/wiki/Hardening)

* **Info:** **ChromeOS** uses the Open-Network-Configuration (_ONC_) format.

  It is formatted in JSON and pretty hard to debug as you do not get any useful error messages.

  The profile-template provided by this role might not work for every edge-case.

  If you need to troubleshoot it - look into the [ONC documentation](https://chromium.googlesource.com/chromium/src/+/main/components/onc/docs/onc_spec.md#OpenVPN-type).
  But be aware: not every option might work practically as documented..


* **Warning:** If a OpenVPN instance should support connections to **ChromeOS** clients - you will need to set the 'openvpn.instances.[name].security.tls_crypt' option to 'false' as this is not (_currently_) supported by the ChromeOS implementation.


* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** If you want to user `openvpn.unprivileged: true` for [gained system-security](https://openvpn.net/community-resources/hardening-openvpn-security/) the installed OpenVPN binary needs to support `iproute2`!

  The role will check if the binary is compatible and fail is that is not the case!

  **Options how to gain support for iproute2:**

  * You will have to use a binary that was compiled with that option enabled
    * Re-Compile OpenVPN yourself as seen in [this example script](https://github.com/ansibleguy/openvpn-recompiled/blob/main/scripts/build.sh) (_without the 'uninstall'_)
    * Or configure the role to download a re-compiled binary from my [ansibleguy/openvpn-recompiled](https://github.com/ansibleguy/openvpn-recompiled) repository!
  * Uninstall existing OpenVPN packages/binaries
  * Copy/link the `openvpn` binary to `/usr/local/bin`


* **Info:** If you are using multi-factor-authentication you might run into issues when some clients (_like ChromeOS_) do not support a second input field for the second secret!

  You might need to set `openvpn.server.auth.mfa_separator` to any unusual characters you like. (_per example: <<<_)

  This enables you to input both secret1 (_password_) and secret2 (_totp pin_) in the same input field! Like so: `p4ssW0rd<<<001122`

  The default separator `:` will always be supported - even if you set a custom one. This allows both ways to be supported.

## Usage

### Config

Define the config as needed:

```yaml
openvpn:

```

You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* 
*

To debug errors - you can set the 'debug' variable at runtime:
```bash
# WARNING: Will log passwords!
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```

To let **OpenVPN services be automatically restarted** (_without interactive prompts_):
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e auto_restart=yes
```

