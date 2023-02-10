#Get the user to input a number of drones between 1 and 12
badInput = True
while(badInput == True):
    print("How many drones in the swarm? (1-12): ")
    drones = int(input())
    if (drones > 0 and drones < 13):
        badInput = False
    else:
        print("Bad input, please enter a number between 1 and 12")

#Create a docker-compose file Header
f = open("./docker-compose.yaml","w")
f.write("version: '3'\n\n")

f.write("services:\n")

#Mavlink Router
# f.write("  mavlink_router:\n")
# f.write("    image: mavlink_router:latest\n")
# f.write("    container_name: MAVLink_router\n")
# f.write("    ports:\n")
# f.write("      - 6969:4200/udp\n")
# f.write("    links:\n")
# for i in range(1,drones+1):
#     thing_to_write = "      - sitl_" + str(i) + "\n"
#     f.write(thing_to_write)

# f.write("    command: >\n")
# command_params = ""
# for i in range(1,drones + 1):
#     command_params = command_params + "sitl" + str(i) + ":5763 "
# command_string = '      /bin/bash -c " mavlink-routerd ' + command_params + '-e 0.0.0.0:4200"\n'
# f.write(command_string)
# f.write("\n")

#Create a number of sitl containers
for i in range(1,drones + 1):

    ########## COMPOSE THE CONTAINERS FOR EACH SITL INSTANCE ##########
    #Service ID
    thing_to_write = "  sitl_" + str(i) + ":\n"
    f.write(thing_to_write)

    #Which image to use
    thing_to_write = "    image: sitl:latest\n"
    f.write(thing_to_write)

    #Give the container a name
    thing_to_write = "    container_name: sitl" + str(i) + "\n"
    f.write(thing_to_write)

    #set interactive for debugging --  python doesnt like writing these lines
    # thing_to_write('stdin_open: true')
    # f.write(thing_to_write)
    # thing_to_write('tty: true ')
    # f.write(thing_to_write)

    #Port mapping
    thing_to_write = "    ports:\n"
    f.write(thing_to_write)

    #Port for host<-->SITL to GCS
    thing_to_write = '      - "420' + str(i) + ':5760"\n'
    f.write(thing_to_write)
    #Port for host<-->SITL to HRL
    thing_to_write = '      - "410' + str(i) + ':5763"\n'
    f.write(thing_to_write)

    #Mount a volume with the environment variable files into the container
    thing_to_write = '    volumes:\n'
    f.write(thing_to_write)
    thing_to_write = '      - ./env_files:/root/home/env_files\n'
    f.write(thing_to_write)

    #Final command
    thing_to_write = "    command: >\n"
    f.write(thing_to_write)
    #Set the environment variables inside the container
    thing_to_write = '      /bin/bash -c "export $$(cat /root/home/env_files/env' + str(i) + ') &&\n'
    f.write(thing_to_write)
    #Command to start SITL
    thing_to_write = '                    /home/ardupilot/Tools/autotest/sim_vehicle.py --vehicle $${VEHICLE} --custom-location=$${LAT},$${LON},$${ALT},$${DIR} --no-rebuild --no-mavproxy --add-param-file=/home/ardupilot/Tools/autotest/default_params/gazebo-drone' + str(i) + '.parm"'
    f.write(thing_to_write)
    f.write("\n\n")
    
    ########## COMPOSE THE CONTAINERS FOR EACH ROS INSTANCE ##########

    #Container header
    thing_to_write = "  clustering_" + str(i) + ":\n"
    f.write(thing_to_write)

    #Depends on SITL container so mavros has something to attach to 
    f.write("    depends_on:\n")
    thing_to_write = '      - sitl_' + str(i) + '\n'
    f.write(thing_to_write)

    #The image
    f.write("    image: clustering:latest\n")
    thing_to_write = "    container_name: clustering_" + str(i) + "\n"
    f.write(thing_to_write)

    #This is dumb but python doesn't like to store these lines in a variable, so its broken up
    thing_to_write = "    stdi"
    f.write(thing_to_write)
    thing_to_write = "n_open: true\n"
    f.write(thing_to_write)
    thing_to_write = "    tt"
    f.write(thing_to_write)
    thing_to_write = "y: true\n"
    f.write(thing_to_write)
    
    #Bring the env_files over as a volume so they can be sourced and used for ROS
    thing_to_write = "    volumes:\n"
    f.write(thing_to_write)
    thing_to_write = "      - ./env_files:/root/home/env_files\n"
    f.write(thing_to_write)

    #Link for inter-container comms
    f.write("    links:\n")
    thing_to_write = "      - sitl_" + str(i) + "\n"
    f.write(thing_to_write)

    #Command(s) to run on launch
    f.write("    command: >\n")
    f.write('      /bin/bash -c "source /home/catkin_ws/devel/setup.bash &&\n')
    f.write('')
    thing_to_write = "                    export $$(cat /root/home/env_files/ros_env" + str(i) + ")\n"
    f.write(thing_to_write)
    thing_to_write = '                    roslaunch src/clustering_control/launch/clustering_control_container.launch system_ID:=$${SYS_ID} clusterID:=$${CLUSTER_ID} clusterPosition:=$${CLUSTER_POSITION} clusterSize:=$${CLUSTER_SIZE} clusterRadius:=$${CLUSTER_RADIUS} agentAlt:=$${AGENT_ALT} homeLat:=$${HOME_LAT} homeLon:=$${HOME_LON} homeAlt:=$${HOME_ALT} rally1Lat:=$${RALLY1LAT} rally1Lon:=$${RALLY1LON} rally2Lat:=$${RALLY2LAT} rally2Lon:=$${RALLY2LON} fcu_url:=tcp://sitl' + str(i) + ' tgt_system:=$${SYS_ID} tgt_component:=$${COMP_ID}"\n'
    f.write(thing_to_write)


    f.write("\n")