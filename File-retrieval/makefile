# Ports
PEER1_PORT=8001
PEER2_PORT=8002
PEER3_PORT=8003

# File and folder setup
CHUNKS=chunk_0 chunk_1 chunk_2
PEERS=peer1 peer2 peer3
FILE_ID=example_file
OUTPUT=reconstructed_file.txt

.PHONY: all setup run_tracker run_peers run_client clean

all: setup run_tracker run_peers

setup:
	@echo "Creating peer directories and copying chunks..."
	@mkdir -p peer1/chunks peer2/chunks peer3/chunks
	@echo "This is the first part of the file." > chunk_0
	@echo "Here comes the second part." > chunk_1
	@echo "And this is the final part." > chunk_2
	@cp chunk_0 chunk_2 peer1/chunks/
	@cp chunk_0 chunk_1 peer2/chunks/
	@cp chunk_1 chunk_2 peer3/chunks/
	@echo "Setup done."

run_tracker:
	@echo "Starting tracker on port 5000..."
	@python tracker.py &

run_peers:
	@echo "Starting peer servers..."
	@cd peer1 && python ../peer.py $(PEER1_PORT) &
	@cd peer2 && python ../peer.py $(PEER2_PORT) &
	@cd peer3 && python ../peer.py $(PEER3_PORT) &

run_client:
	@echo "Running download client (Bob)..."
	@python download_client.py
	@echo "Reconstructed file contents:"
	@cat $(OUTPUT)

clean:
	@echo "Cleaning up..."
	@rm -rf peer1 peer2 peer3 chunk_0 chunk_1 chunk_2 chunks $(OUTPUT)
	@pkill -f tracker.py || true
	@pkill -f peer.py || true
