# Copyright (C) 2015 Siavoosh Payandeh Azad
# this list contains all the 2D Deadlock-free turn models that provide full connectivity
# for connectivity metric, number of pairs of nodes that can communicate under the
# routing algorithm is used.

#                                                                    Number of       Number of
#                                                                connected pairs   available paths
all_2d_turn_models = [['E2N', 'E2S', 'W2N', 'W2S'],						# 72.0		72.0	XY
                      ['E2N', 'E2S', 'W2N', 'N2E'],						# 72.0		118.0
                      ['E2N', 'E2S', 'W2S', 'S2E'],						# 72.0		118.0
                      ['E2N', 'E2S', 'S2E', 'N2E'],						# 72.0		102.0
                      ['E2N', 'W2N', 'W2S', 'N2W'],						# 72.0		118.0
                      ['E2N', 'W2N', 'N2W', 'N2E'],						# 72.0		102.0
                      ['E2N', 'S2E', 'N2W', 'N2E'],						# 72.0		118.0
                      ['E2S', 'W2N', 'W2S', 'S2W'],						# 72.0		118.0
                      ['E2S', 'W2S', 'S2W', 'S2E'],						# 72.0		102.0
                      ['E2S', 'S2W', 'S2E', 'N2E'],						# 72.0		118.0
                      ['W2N', 'W2S', 'S2W', 'N2W'],						# 72.0		102.0
                      ['W2N', 'S2W', 'N2W', 'N2E'],						# 72.0		118.0
                      ['W2S', 'S2W', 'S2E', 'N2W'],						# 72.0		118.0
                      ['S2W', 'S2E', 'N2W', 'N2E'],						# 72.0		72.0	YX
                      ['E2N', 'E2S', 'W2N', 'W2S', 'S2W'],				# 72.0		152.0
                      ['E2N', 'E2S', 'W2N', 'W2S', 'S2E'],				# 72.0		152.0
                      ['E2N', 'E2S', 'W2N', 'W2S', 'N2W'],				# 72.0		152.0
                      ['E2N', 'E2S', 'W2N', 'W2S', 'N2E'],				# 72.0		152.0
                      ['E2N', 'E2S', 'W2N', 'S2E', 'N2E'],				# 72.0		174.0
                      ['E2N', 'E2S', 'W2N', 'N2W', 'N2E'],				# 72.0		174.0
                      ['E2N', 'E2S', 'W2S', 'S2W', 'S2E'],				# 72.0		174.0
                      ['E2N', 'E2S', 'W2S', 'S2E', 'N2E'],				# 72.0		174.0
                      ['E2N', 'E2S', 'S2W', 'S2E', 'N2E'],				# 72.0		174.0
                      ['E2N', 'E2S', 'S2E', 'N2W', 'N2E'],				# 72.0		174.0
                      ['E2N', 'W2N', 'W2S', 'S2W', 'N2W'],				# 72.0		174.0
                      ['E2N', 'W2N', 'W2S', 'N2W', 'N2E'],				# 72.0		174.0
                      ['E2N', 'W2N', 'S2W', 'N2W', 'N2E'],				# 72.0		174.0
                      ['E2N', 'W2N', 'S2E', 'N2W', 'N2E'],				# 72.0		174.0
                      ['E2N', 'S2W', 'S2E', 'N2W', 'N2E'],				# 72.0		152.0
                      ['E2S', 'W2N', 'W2S', 'S2W', 'S2E'],				# 72.0		174.0
                      ['E2S', 'W2N', 'W2S', 'S2W', 'N2W'],				# 72.0		174.0
                      ['E2S', 'W2S', 'S2W', 'S2E', 'N2W'],				# 72.0		174.0
                      ['E2S', 'W2S', 'S2W', 'S2E', 'N2E'],				# 72.0		174.0
                      ['E2S', 'S2W', 'S2E', 'N2W', 'N2E'],				# 72.0		152.0
                      ['W2N', 'W2S', 'S2W', 'S2E', 'N2W'],				# 72.0		174.0
                      ['W2N', 'W2S', 'S2W', 'N2W', 'N2E'],				# 72.0		174.0
                      ['W2N', 'S2W', 'S2E', 'N2W', 'N2E'],				# 72.0		152.0
                      ['W2S', 'S2W', 'S2E', 'N2W', 'N2E'],				# 72.0		152.0
                      ['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'S2E'],		# 72.0		312.0
                      ['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'N2W'],		# 72.0		312.0
                      ['E2N', 'E2S', 'W2N', 'W2S', 'S2E', 'N2E'],		# 72.0		312.0	West First
                      ['E2N', 'E2S', 'W2N', 'W2S', 'N2W', 'N2E'],		# 72.0		312.0	North Last
                      ['E2N', 'E2S', 'W2N', 'S2E', 'N2W', 'N2E'],		# 72.0		276.0	Negative First
                      ['E2N', 'E2S', 'W2S', 'S2W', 'S2E', 'N2E'],		# 72.0		276.0
                      ['E2N', 'E2S', 'S2W', 'S2E', 'N2W', 'N2E'],		# 72.0		312.0
                      ['E2N', 'W2N', 'W2S', 'S2W', 'N2W', 'N2E'],		# 72.0		276.0
                      ['E2N', 'W2N', 'S2W', 'S2E', 'N2W', 'N2E'],		# 72.0		312.0
                      ['E2S', 'W2N', 'W2S', 'S2W', 'S2E', 'N2W'],		# 72.0		276.0
                      ['E2S', 'W2S', 'S2W', 'S2E', 'N2W', 'N2E'],		# 72.0		312.0
                      ['W2N', 'W2S', 'S2W', 'S2E', 'N2W', 'N2E']]	    # 72.0		312.0