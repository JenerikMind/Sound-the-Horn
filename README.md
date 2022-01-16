# Sound-the-Horn
An open source discord bot keep track of subgroups and make subgroup specific callouts and pings.  Will add other shit over time.  

It uses a python backend to connect to a postgresql server and responds via the discord API.  


COMMANDS

$create group <x> <y> 
<x> is the group name.  Group names SHOULD BE snake case (aka: snake_case).
<y> is the @name(s).  Add as many as you want.  It will group everyone into the created group.

Currently too lazy to create another type of command to add to group, so use the same method to add people on.  There are checks in place to prevent duplicates.


$assemble <x>
$ring_the_alarm <x>
<x> is the message you want to "broadcast" to the subgroup.


$remove <x> from <y>
<x> are the @name(s).  Same as above, add as many as you like you madlad.
<y> is the group name you want them removed from.  Because some men just want to watch the world burn.
