import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_installed_packages(host):
    assert not host.ansible(
        "apt",
        "name=" + "\"{{ uc_install_default_packages + uc_install_extra_packages }}\" " +
        "update_cache=True state=present")["changed"]
