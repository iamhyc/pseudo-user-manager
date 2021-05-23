# Pseudo User for Remote SSH

### 用途
比如你在服务器上只有一个账号，但你想把这个账号共享给一个小组，就可以用这个创建pseudo users

### 原理
pseudo user登陆时，会启动一个shell，并创建和pseudo user home folder相关的的环境变量

### 特性
- 支持本地密码验证（sqlite，可以更换为remote）
