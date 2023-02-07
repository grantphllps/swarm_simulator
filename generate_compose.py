#Get the user to input a number of drones between 1 and 12
badInput = True
while(badInput == True):
    print("How many drones in the swarm? (1-12): ")
    drones = int(input())
    if (drones > 0 and drones < 13):
        badInput = False
    else:
        print("Bad input, please enter a number between 1 and 12")

#Create a docker-compose file
f = open("./docker-compose.yaml","w")
f.write("version: '3'\n\n")
f.write("services:\n")

#Create a number of sitl containers
for i in range(1,drones + 1):

    #Service ID
    thing_to_write = "  sitl" + str(i) + ":\n"
    f.write(thing_to_write)

    #Which image to use
    thing_to_write = "    image: sitl:latest\n"
    f.write(thing_to_write)

    #Give the container a name
    thing_to_write = "    container_name: sitlg" + str(i) + "\n"
    f.write(thing_to_write)

    #set interactive for debugging    
    # thing_to_write('stdin_open: true')
    # f.write(thing_to_write)
    # thing_to_write('tty: true ')
    # f.write(thing_to_write)

    #Port mapping
    thing_to_write = "    ports:\n"
    f.write(thing_to_write)

    #Port for host<-->SITL container
    thing_to_write = '      - "420' + str(i) + ':5760"\n'
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
    

