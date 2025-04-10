# Makefile to open tracker and peers in new Terminal windows (macOS)

.PHONY: run

run:
	@echo "Launching Tracker in a new terminal..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 tracker_server.py"'

	@echo "Launching Peer 1..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server1.py"'

	@echo "Launching Peer 2..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server2.py"'

	@echo "Launching Peer 3..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server3.py"'

	@echo "Launching Peer 4..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server4.py"'

	@echo "Waiting for all servers to start..."
	@sleep 3

	@echo "Running Alice from this terminal..."
	@python3 alice.py
