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
[![Ansible Galaxy](https://img.shields.io/ansible/role/62793)](https://galaxy.ansible.com/ansibleguy/infra_openvpn)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F62793%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/infra_openvpn)


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
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
