# Makefile for P2P File Sharing System (macOS - auto-launch in Terminal)

.PHONY: all help clean run run-tracker run-peers run-alice run-bob

all: help

help:
	@echo "P2P File Sharing System (macOS)"
	@echo ""
	@echo "Available commands:"
	@echo "  make run         - Launch tracker, peers in new terminals, then run Alice"
	@echo "  make run-tracker - Run tracker in a new terminal window"
	@echo "  make run-peers   - Run all peer servers in new terminal windows"
	@echo "  make run-alice   - Run Alice (file sharing)"
	@echo "  make run-bob     - Run Bob (file retrieval)"
	@echo "  make clean       - Clean up generated files"

run:
	@echo "Launching Tracker in a new terminal..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 tracker_server.py"'

	@echo "Launching Peer 1..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server1.py 8001"'

	@echo "Launching Peer 2..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server2.py 8002"'

	@echo "Launching Peer 3..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server3.py 8003"'

	@echo "Launching Peer 4..."
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server4.py 8004"'

	@echo "Waiting for all servers to start..."
	@sleep 3

	@echo "Running Alice from this terminal..."
	@python3 alice.py

	@echo "Running Bob from terminal..."
	@sleep 3 && python3 bob.py

run-tracker:
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 tracker_server.py"'

run-peers:
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server1.py 8001"'
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server2.py 8002"'
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server3.py 8003"'
	@osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && python3 peer_server4.py 8004"'

run-alice:
	@python3 alice.py

run-bob:
	@python3 bob.py

clean:
	@echo "Cleaning up..."
	@rm -rf chunks bob_received_chunks bob_received_file.txt
	@rm -rf peer_8001_chunks peer_8002_chunks peer_8003_chunks peer_8004_chunks
	@echo "Clean up complete!"
