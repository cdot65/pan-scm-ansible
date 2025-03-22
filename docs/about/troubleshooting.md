# Troubleshooting

This guide provides solutions to common issues you might encounter when using the SCM Ansible Collection.

## Authentication Issues

### Symptom: "Authentication Failed" Error

If you receive an authentication error when running playbooks:

1. Verify your credentials:
   ```bash
   echo $PAN_SCM_USERNAME
   echo $PAN_SCM_TENANT
   # Don't echo the password in a shared environment
   ```

2. Check for API timeouts - SCM authentication tokens expire after 30 minutes of inactivity

3. Ensure your tenant ID is correct

4. Try with explicit credentials in your playbook (for testing only):
   ```yaml
   - name: Test connection
     cdot65.scm.address:
       username: "your-username"
       password: "your-password"
       tenant: "your-tenant-id"
       name: "test-connection"
       folder: "SharedFolder"
       ip_netmask: "192.168.1.1/32"
     register: result
     ignore_errors: true
   
   - name: Debug connection result
     debug:
       var: result
   ```

## Module Execution Issues

### Symptom: Module Returns Error About Missing Object

If a module reports a missing object (like a folder or tag that you believe exists):

1. Check the folder path is correct (SCM is case-sensitive)
2. Verify you have permissions to access the object
3. Try running with increased verbosity:
   ```bash
   ansible-playbook your_playbook.yml -vvv
   ```

### Symptom: Changes Not Taking Effect

If your playbook runs successfully but changes aren't reflected in SCM:

1. Remember to commit changes - many modules only stage changes:
   ```yaml
   - name: Commit changes
     cdot65.scm.commit:
       description: "Changes made by Ansible"
   ```

2. Check if the changes are in a candidate configuration not yet pushed:
   ```yaml
   - name: Push candidate configuration
     cdot65.scm.push_config:
       description: "Push changes to firewall"
   ```

## Debug Mode

Enable debug mode to get detailed information:

```yaml
- name: Get address objects with debug
  cdot65.scm.address_info:
    folder: "SharedFolder"
    debug: true
  register: addresses
```

## Common Error Messages

### "Error 403: Forbidden"

- You don't have permission to perform this operation
- Check your role assignment in SCM

### "Error 404: Not Found"

- The API endpoint or resource doesn't exist
- Check folder paths, object names, and API versions

### "Error 400: Bad Request"

- The request data is invalid
- Check required parameters and data formats

## SDK Version Mismatch

If you see errors about missing methods or unexpected behavior:

1. Check your SDK version:
   ```bash
   pip show pan-scm-sdk
   ```

2. Update to the latest version:
   ```bash
   pip install --upgrade pan-scm-sdk
   ```

## Getting Help

If you're still experiencing issues:

1. Check the [GitHub Issues](https://github.com/cdot65/pan-scm-ansible/issues) for similar problems and solutions
2. Submit a detailed bug report with:
    - Collection version (`ansible-galaxy collection list`)
    - SDK version (`pip show pan-scm-sdk`)
    - Python version (`python --version`)
    - Ansible version (`ansible --version`)
    - Full error output (with `-vvv` flag)
    - Steps to reproduce the issue
