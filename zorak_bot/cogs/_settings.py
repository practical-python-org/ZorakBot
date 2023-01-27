import toml
prod = 'server.toml'
test = 'test_server.toml'
############
#  Server  #
############
server_info = toml.load(prod)['server']['info']

############
# Channels #
############
channels = toml.load(prod)['channels']

mod_channel = channels['moderation']
log_channel = channels['log_channel']
normal_channel = channels['normal_channel']

#############
#   Roles   #
#############
user_roles = toml.load(prod)['user_roles']

admin_roles = user_roles['admin']
elevated_roles = user_roles['elevated']
badboi_role = user_roles['bad']
unverified_role = user_roles['unverified']