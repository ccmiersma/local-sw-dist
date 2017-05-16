#This is a script library that can be sourced by bash scripts to define ENV variables and functions.
#

if [ -f /etc/sysconfig/local/environment ]
then
  source /etc/sysconfig/local/environment
fi

function _local_environment {

export LOCAL_SW_ROOT=${LOCAL_SW_ROOT:-/opt/local}


case "$1" in
  set)
    LOCAL_SW_ETC=${LOCAL_SW_ETC:-/etc/opt/local}
    LOCAL_SW_VAR=${LOCAL_SW_VAR:-/var/opt/local}
    LOCAL_SW_SCRIPT_LIBS=${LOCAL_SW_SCRIPT_LIBS:-/opt/local/lib/scripts}

    export LOCAL_SW_ETC
    export LOCAL_SW_VAR
    export LOCAL_SW_SCRIPT_LIBS
    export PATH=$PATH:$LOCAL_SW_ROOT/bin:$LOCAL_SW_ROOT/sbin
    export MANPATH=:$LOCAL_SW_ROOT/share/man
    ;;
  unset)
    # Strip out PATH addition for /bin
    export PATH=${PATH//$LOCAL_SW_ROOT\/bin/}
    
    # Strip out PATH addition for /sbin
    export PATH=${PATH//$LOCAL_SW_ROOT\/sbin/}
    
    # Remove trailing : twice for each path
    export PATH=${PATH%:}
    export PATH=${PATH%:}
    # Remove leading :
    export PATH=${PATH#:}
    export PATH=${PATH#:}
    
    unset MANPATH
    unset LOCAL_SW_ETC
    unset LOCAL_SW_VAR
    unset LOCAL_SW_SCRIPT_LIBS
    unset LOCAL_SW_ROOT
    ;;
  path_override)
    export PATH=$LOCAL_SW_ROOT/bin:$LOCAL_SW_ROOT/sbin:$PATH
    export MANPATH=$LOCAL_SW_ROOT/share/man:
    ;;
  *)
    echo "The following LOCAL environmental variables are defined."
    env | grep LOCAL_*
    ;;

esac

}

