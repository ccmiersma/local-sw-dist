Local Software Distribution
===========================

This package will install the base environment for a custom software distribution.
This can serve as a starting point for a complete integrated set of scripts, configurations,
and custom applications local to your organization.

This sets up a software tree similar to /usr/ or /usr/local under /opt/local, or
the path of your choice. This allows packaged scripts to be easily distinguished
from the operating system and third-party vendors.

The configuration is added to the environment through 3 files:
1. A set of environmental variables in /etc/sysconfig/local/environment
2. A library of bash functions in /opt/local/lib/scripts that uses variables defined in /etc/sysconfig/local/environment


The files are sourced in that order by a profile script. All variables beginning in LOCAL_ are exported. These are normally defined in /etc/sysconfig/local/environment. By default this is LOCAL_SW_ROOT, LOCAL_SW_ETC, LOCAL_SW_VAR, and LOCAL_SW_SCRIPT_LIBS, all of which will be defined even if the environment file is empty. The _local_environment function is also defined. This function will export or unset the variables as needed. The environment file is marked as config(noreplace) so that it can be customized without being changed on update. 
