# ubuntu-common

## 目次

<!-- TOC depthFrom:2 -->

- [目次](#目次)
- [概要](#概要)
- [動作確認バージョン](#動作確認バージョン)
- [使い方 (ansible)](#使い方-ansible)
    - [Role variables](#role-variables)
    - [Example playbook](#example-playbook)
- [後方互換性について](#後方互換性について)
    - [削除された変数の一覧](#削除された変数の一覧)
    - [変更された変数の一覧](#変更された変数の一覧)
- [Licence](#licence)

<!-- /TOC -->

<br>

## 概要

ubuntu の基本設定や追加パッケージをインストールする ansible role

<br>

## 動作確認バージョン
- Ubuntu 18.04 (bionic)
- ansible >= 2.8
- Jinja2 2.10.3

<br>

## 使い方 (ansible)

### Role variables

```yaml
## インストールフラグ
#  * False にすると install.yml をスキップできる.
#  * install.yml 以外を流し込みたいときに使う.
#  * install.yml の中には apt 関係のモジュールが書き込まれている.
uc_install_flag: True

## インストールパッケージ (デフォルト)
#   * 滅多に変更しない.
#   * インストールしたくないパッケージがあるなら修正するくらい.
uc_install_default_packages:
  - "openssh-server"
  - "dstat"
  - "vim"
  - "htop"
  - "curl"
  - "wget"
  - "zip"
  - "unzip"
  - "git"
  - "tzdata"
  - "python3-pip"
  - "language-pack-ja"
  - "nvme-cli"
  - "smartmontools"

## インストールパッケージ (外部から拡張 ※ group_vars 等)
#  * リスト形式でパッケージを指定
uc_install_extra_packages: []
# 設定例
# uc_install_extra_packages:
#   - "gcc"
#   - "g++"

## OS の基本設定
uc_change_hostname: yes
uc_change_timezone: no
uc_change_sshd_config: yes
uc_default_system_timezone: "Asia/Tokyo"

## sshd_config の基本設定
uc_sshd_port: "22"
uc_sshd_password_auth: "no"   # ブール値ではなく文字列で指定
uc_sshd_match_configs: []
### 設定例
# uc_sshd_match_configs:
#   - type: User
#     pattern: linux_user
#     lines:
#       - PasswordAuthentication yes

## カーネルパラメータを変更するかどうかの判定
uc_change_sysctl_parameter: yes
## カーネルパラメータ (デフォルト値)
uc_sysctl_parameters:
  net.core.rmem_max: 16777216
  net.core.wmem_max: 16777216
  net.core.rmem_default: 16777216
  net.core.wmem_default: 16777216
  net.core.optmem_max: 40960
  net.ipv4.tcp_rmem: 4096 87380 16777216
  net.ipv4.tcp_wmem: 4096 65536 16777216
  net.core.netdev_max_backlog: 65535
  net.core.somaxconn: 65535
  net.ipv4.tcp_max_syn_backlog: 65535
  net.ipv4.tcp_max_tw_buckets: 200000
  net.ipv4.tcp_slow_start_after_idle: 0
  net.ipv4.tcp_abort_on_overflow: 1
  net.ipv4.tcp_tw_reuse: 1
  net.ipv4.tcp_fin_timeout: 30
  net.ipv4.ip_local_port_range: 10000 65535
  fs.aio-max-nr: 1048576
# カーネルパラメータの他の設定例
# 一部だけ指定したり, defaults/main.yml に無いカーネルパラメータも指定できる.
# uc_sysctl_parameters:
#   fs.inotify.max_user_watches: 5000000
#   net.netfilter.nf_conntrack_max: 10000000
#   net.nf_conntrack_max: 10000000
#   net.netfilter.nf_conntrack_tcp_timeout_established: 86400
#   net.netfilter.nf_conntrack_tcp_timeout_time_wait: 10
#   net.netfilter.nf_conntrack_buckets: 1250000

## apport 関係
# * PHP-fpm がクラッシュしたときに apport 機能の権限周りでエラーになるため、
#   apport 機能を OFF にできるようにする
# * local など apport がない環境では change_default_apport を false にする
uc_change_default_apport: False
uc_disable_apport: False
```

<br>

### Example playbook
```yaml
- hosts:
    - servers
  become: True
  roles:
    - { role: ubuntu-common,   tags: ["ubuntu-common"] }
```

<br>

## 後方互換性について

### 削除された変数の一覧

以下の変数は `group_vars` から削除して頂いて大丈夫です.

* `sshd_port`
  * ポート開放はすべて ufw role で実行する方針に切り替えたため削除しました.

<br>

### 変更された変数の一覧

`group_vars` において以下のように新しい書き方に変えて頂いて大丈夫です.

* `ubuntu_common_install_default_packages` → `uc_install_default_packages`
* `ubuntu_common_install_extra_packages` → `uc_install_extra_packages`
* `change_hostname` → `uc_change_hostname`
* `change_timezone` → `uc_change_timezone`
* `change_sshd_config` → `uc_change_sshd_config`
* `default_system_timezone` → `uc_default_system_timezone`
* `sshd_password_auth` → `uc_sshd_password_auth`
* `sshd_match_configs` → `uc_sshd_match_configs`
* `change_sysctl_parameter` → `uc_change_sysctl_parameter`
* `sysctl_parameters` → `uc_sysctl_parameters`
* `ubuntu_common_change_default_apport` → `uc_change_default_apport`
* `ubuntu_common_disable_apport` → `uc_disable_apport`

<br>

## Licence
MIT
