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

#Create the Networks
f.write("networks:\n")

#Create a network for each ROS<-->SITL par
for i in range(1,drones + 1):
    thing_to_write = '  agent_' + str(i) + '_net:\n'
    f.write(thing_to_write)
    f.write("    ipam:\n")
    f.write("      config:\n")
    f.write("        - subnet: 172.20." + str(i) + ".0/24\n")
    f.write("\n")

#Create the SITL, ARL, and MAVlink router services
f.write("services:\n")

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
    thing_to_write = "    container_name: sitlg" + str(i) + "\n"
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

    #Add the container to the newtork
    f.write("    networks:\n")
    thing_to_write = "      agent_" + str(i) + "_net:\n"
    f.write(thing_to_write)
    thing_to_write = "        ipv4_address: 172.20." + str(i) + ".7\n"
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
    thing_to_write = '                    /ardupilot/Tools/autotest/sim_vehicle.py --vehicle $${VEHICLE} -I$${INSTANCE} --custom-location=$${LAT},$${LON},$${ALT},$${DIR} -w --frame $${MODEL} --no-rebuild --no-mavproxy --speedup $${SPEEDUP} --add-param-file=/ardupilot/Tools/autotest/default_params/gazebo-drone' + str(i) + '.parm"'
    f.write(thing_to_write)
    f.write("\n\n")
    
    ########## COMPOSE THE CONTAINERS FOR EACH ROS INSTANCE ##########
    thing_to_write = "  clustering_" + str(i) + ":\n"
    f.write(thing_to_write)
    f.write("    depends_on:\n")
    thing_to_write = '      - sitl_' + str(i) + '\n'
    f.write(thing_to_write)
    f.write("    image: clustering:latest\n")
    thing_to_write = "    container_name: clustering_" + str(i) + "\n"
    f.write(thing_to_write)
    thing_to_write = "    stdi"
    f.write(thing_to_write)
    thing_to_write = "n_open: true\n"
    f.write(thing_to_write)
    thing_to_write = "    tt"
    f.write(thing_to_write)
    thing_to_write = "y: true\n"
    f.write(thing_to_write)
    thing_to_write = "    volumes:\n"
    f.write(thing_to_write)
    thing_to_write = "      - /home/ubuntu/rosbags:/home/rosbags\n"
    f.write(thing_to_write)
    thing_to_write = "      - ./env_files:/root/home/env_files\n"
    f.write(thing_to_write)
    f.write("    networks:\n")
    thing_to_write = "      agent_" + str(i) + "_net:\n"
    f.write(thing_to_write)
    thing_to_write = "        ipv4_address: 172.20." + str(i) + ".6\n"
    f.write(thing_to_write)
    f.write("    command: >\n")
    f.write('      /bin/bash -c "source /home/catkin_ws/devel/setup.bash &&\n')
    f.write('')
    thing_to_write = "                    export $$(cat /root/home/env_files/ros_env" + str(i) + ")\n"
    f.write(thing_to_write)
    thing_to_write = '                    roslaunch src/clustering_control/launch/clustering_control_container.launch system_ID:=$${SYS_ID} clusterID:=$${CLUSTER_ID} clusterPosition:=$${CLUSTER_POSITION} clusterSize:=$${CLUSTER_SIZE} clusterRadius:=$${CLUSTER_RADIUS} agentAlt:=$${AGENT_ALT} homeLat:=$${HOME_LAT} homeLon:=$${HOME_LON} homeAlt:=$${HOME_ALT} rally1Lat:=$${RALLY1LAT} rally1Lon:=$${RALLY1LON} rally2Lat:=$${RALLY2LAT} rally2Lon:=$${RALLY2LON} fcu_url:=$${PORT} tgt_system:=$${SYS_ID} tgt_component:=$${COMP_ID}"'
    f.write(thing_to_write)


    f.write("\n")