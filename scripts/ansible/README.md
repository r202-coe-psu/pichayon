How to use ansible to update hosts
`
1. add hosts to /etc/hosts
2. source venv/bin/activate
3. cd pichayon/scripts/ansible
4. ansible-galaxy collection install -r requirements.yml
5. run command: ansible-playbook ansible_playbooks/setup-ssh-key.yml -i ansible-inventory.yml -k
   (installs this PC's SSH key on each host; -k prompts for the pcy user's SSH password, needs sshpass installed locally; only needs to be run once per host)
6. run command: ansible-playbook ansible_playbooks/deploy-pichayon.yml -i ansible-inventory.yml
7. wait for ansible completed all tasks
`