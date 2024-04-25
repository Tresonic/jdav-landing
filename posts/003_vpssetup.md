# VPS Setup

- update
- change root password if not set already

### Add user with sudo privileges
```adduser vpsadmin```
```usermod -aG sudo vpsadmin```

### SSH Setup
In `/etc/ssh/sshd_config`:
```
Port 62222
Protocol 2
PermitRootLogin no
AllowUsers vpsadmin
```

Use Keys for Auth with passphrase and name for key:

```
ssh-keygen -N 'securepassphrase' -t ed25519 -C 'mycomputer'
chmod 0600 /home/vpsadmin/.ssh/authorized_keys
```
optionally set `PasswordAuthentication no` in `/etc/ssh/sshd_config`

Add Alias on Client in `~/.ssh/config`:
```
Host 1.1.1.1
  User vpsadmin
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  Port 62222
```
Remove `AcceptEnv LANG LC_*` to silence perl LC warnings

### Firewall Setup
```
ufw allow 62222/tcp
ufw enable
```

### Setup Hostname
```
hostnamectl set-hostname newhostname
```
In `/etc/hosts`:
```
127.0.1.1 newhostname
```

### Change shell
```
apt install zsh
chsh -s $(which zsh)
```
Install omz:
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
set theme in `.zshrc`:
```
ZSH_THEME=bira
```

### Packages
```git```
