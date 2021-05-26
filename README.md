# Pseudo User for Remote SSH
> 还有点问题，请不要使用本仓库

### 用途
比如你在服务器上只有一个账号，但你想把这个账号共享给一个小组，就可以用这个创建pseudo users；

安装后，只需要在启动的shell profile最后加上以下内容即可。

```bash
if [ -n "$PSEUDO_USER" ] && [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
  exec pseudo-switch
fi
```

### 原理
pseudo user登录时，会启动一个shell，并创建和pseudo user home folder相关的的环境变量

### 特性
- 支持仅在必要时在登录后切换到pseudo home目录
- 支持本地密码验证（sqlite，可以更换为remote）

### Todos
- 修复密码保存问题
- 支持通过known host public key免密码直接登录
