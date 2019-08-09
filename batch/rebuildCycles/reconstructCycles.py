"""reconstruct blender Beauty pass using Diffuse, Gloss, SSS, Transmission, Emission and Environment passes"""

def get_batch_custom_ui_actions():
    """Return custom actions to execute on Batch objects."""

    def scope_node(selection):
        """Scope the custom action to the nodes residing in a Batch Schematic."""
        import flame
        for item in selection:
            if isinstance(item, flame.PyNode):
            	if item.type == "Clip":
                	return True
        return False

    def reconstructCycles(selection):
		import string
		import flame

		# get selected clip in batch
		clipNode = flame.batch.current_node.get_value()

		# get selected clip name
		clipName = clipNode.name

		previousNode = clipNode

		# node position offsets at creation time
		addXoffset = 500
		addYoffset = 700

		multXoffset = addXoffset + 100
		multYoffset = addYoffset - 200

		# create empty PyNode list
		FULLcompNodes = []


		# cycle through all output sockets of selected node
		for outSocket in clipNode.output_sockets:


			##########################################
			#           REBUILD DIFFUSE PASS         #
			##########################################

			# check if 'Diff' is in render pass name
			if 'Diff' in outSocket:

				# find 'Color' render pass
				if 'Col' in outSocket:

					diffuseColSocket = outSocket

					# create a 'Comp' node for FULL pass reconstruction
					FULLdiffuseCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					FULLdiffuseCompNode.flame_blend_mode = "Multiply"

					# connect 'Front' to 'Col' render pass
					flame.batch.connect_nodes(clipNode, diffuseColSocket, FULLdiffuseCompNode, "Front")

					# set node position
					FULLdiffuseCompNode.pos_x = previousNode.pos_x + multXoffset
					FULLdiffuseCompNode.pos_y = previousNode.pos_y - multYoffset

				# find 'Direct' render pass
				if 'Dir' in outSocket:

					diffuseDirectSocket = outSocket

					# create a 'Comp' node for RAW pass reconstruction
					RAWdiffuseCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					RAWdiffuseCompNode.flame_blend_mode = "Add"

					# connect 'Front' to 'Direct' render pass
					flame.batch.connect_nodes(clipNode, diffuseDirectSocket, RAWdiffuseCompNode, "Front")

					# set node position
					RAWdiffuseCompNode.pos_x = previousNode.pos_x + addXoffset
					RAWdiffuseCompNode.pos_y = previousNode.pos_y - addYoffset


				# find 'Indirect' render pass
				if 'Ind' in outSocket:

					diffuseIndirectSocket = outSocket

					# connect 'Indirect' render pass to 'Back'
					flame.batch.connect_nodes(clipNode, diffuseIndirectSocket, RAWdiffuseCompNode, "Back")

					# connect RAW node to FULL nodediffuseIndirectSocket
					flame.batch.connect_nodes(RAWdiffuseCompNode, 'Result', FULLdiffuseCompNode, "Back")

					FULLcompNodes.append(FULLdiffuseCompNode)

					previousNode = FULLdiffuseCompNode

					# CREATE COMPASS FOR DIFFUSE
					diffuseCompass = flame.batch.create_node("Compass")

					diffuseCompass.name = 'DIFFUSE_' + clipName

					diffuseCompass.pos_x = RAWdiffuseCompNode.pos_x -200
					diffuseCompass.pos_y = RAWdiffuseCompNode.pos_y -150

					diffuseCompass.width = 550
					diffuseCompass.height = 550

					diffuseCompass.colour = (0.13,0.2,0.13)


			########################################
			#          REBUILD GLOSS PASS          #
			########################################

			# check if 'Gloss' is in render pass name
			if 'Gloss' in outSocket:

				# find 'Color' render pass
				if 'Col' in outSocket:

					glossColSocket = outSocket

					# create a 'Comp' node for FULL pass reconstruction
					FULLglossCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					FULLglossCompNode.flame_blend_mode = "Multiply"

					# connect 'Front' to 'Col' render pass
					flame.batch.connect_nodes(clipNode, glossColSocket, FULLglossCompNode, "Front")

					# set node position
					FULLglossCompNode.pos_x = previousNode.pos_x + multXoffset
					FULLglossCompNode.pos_y = previousNode.pos_y - multYoffset

				# find 'Direct' render pass
				if 'Dir' in outSocket:

					glossDirectSocket = outSocket

					# create a 'Comp' node for RAW pass reconstruction
					RAWglossCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					RAWglossCompNode.flame_blend_mode = "Add"

					# connect 'Front' to 'Direct' render pass
					flame.batch.connect_nodes(clipNode, glossDirectSocket, RAWglossCompNode, "Front")

					# set node position
					RAWglossCompNode.pos_x = previousNode.pos_x + addXoffset
					RAWglossCompNode.pos_y = previousNode.pos_y - addYoffset


				# find 'Indirect' render pass
				if 'Ind' in outSocket:

					glossIndirectSocket = outSocket

					# connect 'Indirect' render pass to 'Back'
					flame.batch.connect_nodes(clipNode, glossIndirectSocket, RAWglossCompNode, "Back")

					# connect RAW node to FULL node
					flame.batch.connect_nodes(RAWglossCompNode, 'Result', FULLglossCompNode, "Back")

					FULLcompNodes.append(FULLglossCompNode)

					previousNode = FULLglossCompNode

					# CREATE COMPASS FOR DIFFUSE
					glossCompass = flame.batch.create_node("Compass")

					glossCompass.pos_x = RAWglossCompNode.pos_x -200
					glossCompass.pos_y = RAWglossCompNode.pos_y -150

					glossCompass.width = 550
					glossCompass.height = 550

					glossCompass.name = 'GLOSS_' + clipName

					glossCompass.colour = (0.25,0.0,0.25)




			#############################################
			#           REBUILD SUBSURFACE PASS         #
			#############################################

			# check if 'Subsurface' is in render pass name
			if 'Subsurface' in outSocket:

				# find 'Color' render pass
				if 'Col' in outSocket:

					subsurfaceColSocket = outSocket

					# create a 'Comp' node for FULL pass reconstruction
					FULLSubsurfaceCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					FULLSubsurfaceCompNode.flame_blend_mode = "Multiply"

					# connect 'Front' to 'Col' render pass
					flame.batch.connect_nodes(clipNode, subsurfaceColSocket, FULLSubsurfaceCompNode, "Front")

					# set node position
					FULLSubsurfaceCompNode.pos_x = previousNode.pos_x + multXoffset
					FULLSubsurfaceCompNode.pos_y = previousNode.pos_y - multYoffset

				# find 'Direct' render pass
				if 'Dir' in outSocket:

					subsurfaceDirectSocket = outSocket

					# create a 'Comp' node for RAW pass reconstruction
					RAWsubsurfaceCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					RAWsubsurfaceCompNode.flame_blend_mode = "Add"

					# connect 'Front' to 'Direct' render pass
					flame.batch.connect_nodes(clipNode, subsurfaceDirectSocket, RAWsubsurfaceCompNode, "Front")

					# set node position
					RAWsubsurfaceCompNode.pos_x = previousNode.pos_x + addXoffset
					RAWsubsurfaceCompNode.pos_y = previousNode.pos_y - addYoffset


				# find 'Indirect' render pass
				if 'Ind' in outSocket:

					subsurfaceIndirectSocket = outSocket

					# connect 'Indirect' render pass to 'Back'
					flame.batch.connect_nodes(clipNode, subsurfaceIndirectSocket, RAWsubsurfaceCompNode, "Back")


					# connect RAW node to FULL nodediffuseIndirectSocket
					flame.batch.connect_nodes(RAWsubsurfaceCompNode, 'Result', FULLSubsurfaceCompNode, "Back")


					FULLcompNodes.append(FULLSubsurfaceCompNode)


					previousNode = FULLSubsurfaceCompNode

					# CREATE COMPASS FOR SUBSURFACE
					subsurfaceCompass = flame.batch.create_node("Compass")

					subsurfaceCompass.name = 'SSS_' + clipName

					subsurfaceCompass.pos_x = RAWsubsurfaceCompNode.pos_x -200
					subsurfaceCompass.pos_y = RAWsubsurfaceCompNode.pos_y -150

					subsurfaceCompass.width = 550
					subsurfaceCompass.height = 550

					subsurfaceCompass.colour = (0.13,0.24,0.24)



			###############################################
			#           REBUILD TRANSMISSION PASS         #
			###############################################

			# check if 'Transmission' is in render pass name
			if 'Trans' in outSocket:

				# find 'Color' render pass
				if 'Col' in outSocket:

					transmissionColSocket = outSocket

					# create a 'Comp' node for FULL pass reconstruction
					FULLtransmissionCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					FULLtransmissionCompNode.flame_blend_mode = "Multiply"

					# connect 'Front' to 'Col' render pass
					flame.batch.connect_nodes(clipNode, transmissionColSocket, FULLtransmissionCompNode, "Front")

					# set node position
					FULLtransmissionCompNode.pos_x = previousNode.pos_x + multXoffset
					FULLtransmissionCompNode.pos_y = previousNode.pos_y - multYoffset

				# find 'Direct' render pass
				if 'Dir' in outSocket:

					transmissionDirectSocket = outSocket

					# create a 'Comp' node for RAW pass reconstruction
					RAWtransmissionCompNode = flame.batch.create_node("Comp")

					# set RAW 'Comp' node to 'Add'
					RAWtransmissionCompNode.flame_blend_mode = "Add"

					# connect 'Front' to 'Direct' render pass
					flame.batch.connect_nodes(clipNode, transmissionDirectSocket, RAWtransmissionCompNode, "Front")

					# set node position
					RAWtransmissionCompNode.pos_x = previousNode.pos_x + addXoffset
					RAWtransmissionCompNode.pos_y = previousNode.pos_y - addYoffset


				# find 'Indirect' render pass
				if 'Ind' in outSocket:

					transmissionIndirectSocket = outSocket

					# connect 'Indirect' render pass to 'Back'
					flame.batch.connect_nodes(clipNode, transmissionIndirectSocket, RAWtransmissionCompNode, "Back")


					# connect RAW node to FULL nodediffuseIndirectSocket
					flame.batch.connect_nodes(RAWtransmissionCompNode, 'Result', FULLtransmissionCompNode, "Back")


					FULLcompNodes.append(FULLtransmissionCompNode)


					previousNode = FULLtransmissionCompNode

					# CREATE COMPASS FOR TRANSMISSION
					transmissionCompass = flame.batch.create_node("Compass")

					transmissionCompass.name = 'TRANSMISSION_' + clipName

					transmissionCompass.pos_x = RAWtransmissionCompNode.pos_x -200
					transmissionCompass.pos_y = RAWtransmissionCompNode.pos_y -150

					transmissionCompass.width = 550
					transmissionCompass.height = 550

					transmissionCompass.colour = (0.45,0.16,0.16)




		# comp all reconstructed passes
		if len(FULLcompNodes) >= 2 :

			firstNode = True

			counter = 0

			while counter < (len(FULLcompNodes)-1):

				print counter

				addNode = flame.batch.create_node("Comp")
				addNode.flame_blend_mode = "Add"

				

				if firstNode == True:
					flame.batch.connect_nodes(FULLcompNodes[counter], "Result", addNode, "Front")
					flame.batch.connect_nodes(FULLcompNodes[counter+1], "Result", addNode, "Back")

					addNode.pos_x = FULLcompNodes[counter].pos_x + multXoffset + 400
					addNode.pos_y = FULLcompNodes[counter].pos_y

					previousNode = addNode

				else :
					flame.batch.connect_nodes(previousNode, "Result", addNode, "Front")
					flame.batch.connect_nodes(FULLcompNodes[counter+1], "Result", addNode, "Back")

					addNode.pos_x = FULLcompNodes[counter].pos_x + multXoffset + 400
					addNode.pos_y = previousNode.pos_y

					previousNode = addNode
						

				counter += 1
				firstNode = False


		# cycle through all output sockets of selected node
		for outSocket in clipNode.output_sockets:

			###############################################
			#               ADD EMISSION PASS             #
			###############################################

			# check if 'Emission' is in render pass name
			if 'Emit' in outSocket:

				emissionColSocket = outSocket

				# create a 'Comp' node for Emission pass
				emissionCompNode = flame.batch.create_node("Comp")

				# set Emission 'Comp' node to 'Add'
				emissionCompNode.flame_blend_mode = "Add"

				# connect 'Front' to 'Col' render pass
				flame.batch.connect_nodes(clipNode, emissionColSocket, emissionCompNode, "Front")
				flame.batch.connect_nodes(previousNode, 'Result', emissionCompNode, "Back")

				# set node position
				emissionCompNode.pos_x = previousNode.pos_x + multXoffset
				emissionCompNode.pos_y = previousNode.pos_y + multYoffset

				previousNode = emissionCompNode


				# CREATE COMPASS FOR EMISSION
				emissionCompass = flame.batch.create_node("Compass")

				emissionCompass.name = 'EMISSION_' + clipName

				emissionCompass.width = 400
				emissionCompass.height = 400

				emissionCompass.pos_x = emissionCompNode.pos_x - (emissionCompass.width/2)
				emissionCompass.pos_y = emissionCompNode.pos_y - (emissionCompass.height/2)

				emissionCompass.colour = (0.15,0.08,0.43)

			###############################################
			#               ADD ENVIRONMENT PASS          #
			###############################################

			# check if 'Transmission' is in render pass name
			if 'Env' in outSocket:

				environmentSocket = outSocket

				# create a 'Comp' node for Emission pass
				environmentCompNode = flame.batch.create_node("Comp")

				# set Emission 'Comp' node to 'Add'
				environmentCompNode.flame_blend_mode = "Add"

				# connect 'Front' to 'Col' render pass
				flame.batch.connect_nodes(clipNode, environmentSocket, environmentCompNode, "Front")
				flame.batch.connect_nodes(previousNode, 'Result', environmentCompNode, "Back")


				# set node position
				environmentCompNode.pos_x = previousNode.pos_x + multXoffset
				environmentCompNode.pos_y = previousNode.pos_y + multYoffset

				previousNode = environmentCompNode


				# CREATE COMPASS FOR ENVIRONMENT
				environmentCompass = flame.batch.create_node("Compass")

				environmentCompass.name = 'ENVIRONMENT_' + clipName

				environmentCompass.width = 400
				environmentCompass.height = 400

				environmentCompass.pos_x = environmentCompNode.pos_x - (environmentCompass.width/2)
				environmentCompass.pos_y = environmentCompNode.pos_y - (environmentCompass.height/2)

				environmentCompass.colour = (0.15,0.25,0.43)


    return [
        {
            "name": "PYTHON: NODES",
            "actions": [
                {
                    "name": "Reconstruct Blender Beauty",
                    "isVisible": scope_node,
                    "execute": reconstructCycles
                }
            ]
        }
    ]
