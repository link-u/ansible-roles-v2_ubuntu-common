import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_hostname(host):
    ## NOTE:ホスト名の取得について
    #  * https://qiita.com/satton6987/items/f50ad3df302290d1f544
    ansible_vars = host.ansible.get_variables()
    inventory_hostname = ansible_vars["inventory_hostname"]
    hostname = host.run("uname -n").stdout
    hostname = hostname[:-1]   # 改行文字の削除
    assert inventory_hostname == hostname

def test_timezone(host):
    ansible_vars = host.ansible.get_variables()
    timezone = ansible_vars["uc_default_system_timezone"]
    assert host.file("/etc/localtime").exists
    assert host.file("/etc/localtime").is_symlink
    assert host.run("cat /etc/timezone").stdout == (timezone + "\n")
