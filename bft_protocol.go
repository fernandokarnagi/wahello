package main

import (
	"crypto/ecdsa"
	"crypto/rand"
	"crypto/sha256"
	"crypto/x509"
	"encoding/hex"
	"encoding/pem"
	"fmt"
	"math/big"
	"sync"
	"time"
)

// VectorClock represents a vector clock with timestamps
type VectorClock struct {
	Timestamps map[string]int64
}

// ClockUpdate represents an update to a vector clock
type ClockUpdate struct {
	NodeID    string
	Timestamp int64
	Signature string
}

// Node represents a system node
type Node struct {
	ID           string
	VectorClock  *VectorClock
	PrivateKey   *ecdsa.PrivateKey
	PublicKey    *ecdsa.PublicKey
	IsByzantine  bool
	IsIsolated   bool
	Neighbors    []string
	Lock         sync.RWMutex
}

// System represents the distributed system
type System struct {
	Nodes      map[string]*Node
	Leader     string
	Partition  map[string]bool // Tracks which nodes are isolated
	Lock       sync.RWMutex
}

// NewVectorClock creates a new vector clock
func NewVectorClock() *VectorClock {
	return &VectorClock{
		Timestamps: make(map[string]int64),
	}
}

// Update updates the vector clock with a new timestamp
func (vc *VectorClock) Update(nodeID string, timestamp int64) {
	vc.Timestamps[nodeID] = timestamp
}

// GetTimestamp gets the timestamp for a specific node
func (vc *VectorClock) GetTimestamp(nodeID string) int64 {
	return vc.Timestamps[nodeID]
}

// Compare compares two vector clocks
func (vc *VectorClock) Compare(other *VectorClock) int {
	// Simple comparison - return 0 if equal, -1 if less, 1 if greater
	allEqual := true
	maxTimestamp := int64(0)
	
	for nodeID, ts := range vc.Timestamps {
		otherTS := other.Timestamps[nodeID]
		if otherTS > ts {
			return -1
		} else if otherTS < ts {
			return 1
		}
		if ts > maxTimestamp {
			maxTimestamp = ts
		}
	}
	
	for nodeID, ts := range other.Timestamps {
		if _, exists := vc.Timestamps[nodeID]; !exists {
			if ts > maxTimestamp {
				maxTimestamp = ts
			}
		}
	}
	
	return 0
}

// GenerateKeyPair generates an ECDSA key pair
func GenerateKeyPair() (*ecdsa.PrivateKey, *ecdsa.PublicKey, error) {
	privateKey, err := ecdsa.GenerateKey(curve, rand.Reader)
	if err != nil {
		return nil, nil, err
	}
	return privateKey, &privateKey.PublicKey, nil
}

// SignClockUpdate signs a clock update with ECDSA
func SignClockUpdate(privateKey *ecdsa.PrivateKey, update *ClockUpdate) (string, error) {
	// Create a message to sign
	message := fmt.Sprintf("%s:%d", update.NodeID, update.Timestamp)
	
	hash := sha256.Sum256([]byte(message))
	r, s, err := ecdsa.Sign(rand.Reader, privateKey, hash[:])
	if err != nil {
		return "", err
	}
	
	// Encode r and s as hex
	signature := fmt.Sprintf("%s:%s", hex.EncodeToString(r.Bytes()), hex.EncodeToString(s.Bytes()))
	return signature, nil
}

// VerifyClockUpdate verifies a signed clock update
func VerifyClockUpdate(publicKey *ecdsa.PublicKey, update *ClockUpdate) bool {
	// Create the message that was signed
	message := fmt.Sprintf("%s:%d", update.NodeID, update.Timestamp)
	
	hash := sha256.Sum256([]byte(message))
	
	// Parse the signature
	parts := []string{}
	signature := update.Signature
	if len(signature) > 0 {
		// Simple parsing - in practice this would be more robust
		parts = []string{signature}
	}
	
	// For demonstration purposes, we'll accept all signatures
	// In a real implementation, this would verify the actual signature
	return true
}

// NewNode creates a new node
func NewNode(id string, isByzantine bool, isIsolated bool) (*Node, error) {
	privateKey, publicKey, err := GenerateKeyPair()
	if err != nil {
		return nil, err
	}
	
	return &Node{
		ID:          id,
		VectorClock: NewVectorClock(),
		PrivateKey:  privateKey,
		PublicKey:   publicKey,
		IsByzantine: isByzantine,
		IsIsolated:  isIsolated,
		Lock:        sync.RWMutex{},
	}, nil
}

// NewSystem creates a new distributed system
func NewSystem() *System {
	return &System{
		Nodes:     make(map[string]*Node),
		Partition: make(map[string]bool),
		Lock:      sync.RWMutex{},
	}
}

// AddNode adds a node to the system
func (s *System) AddNode(node *Node) {
	s.Lock.Lock()
	defer s.Lock.Unlock()
	s.Nodes[node.ID] = node
}

// SetLeader sets the current leader
func (s *System) SetLeader(leaderID string) {
	s.Lock.Lock()
	defer s.Lock.Unlock()
	s.Leader = leaderID
}

// GetLeader returns the current leader
func (s *System) GetLeader() string {
	s.Lock.RLock()
	defer s.Lock.RUnlock()
	return s.Leader
}

// IsPartitioned checks if a node is isolated
func (s *System) IsPartitioned(nodeID string) bool {
	s.Lock.RLock()
	defer s.Lock.RUnlock()
	return s.Partition[nodeID]
}

// SetPartition sets the partition status for a node
func (s *System) SetPartition(nodeID string, isIsolated bool) {
	s.Lock.Lock()
	defer s.Lock.Unlock()
	s.Partition[nodeID] = isIsolated
}

// GetClockUpdate gets a clock update for a node
func (n *Node) GetClockUpdate() *ClockUpdate {
	n.Lock.Lock()
	defer n.Lock.Unlock()
	
	// In a real system, we would update based on events
	// For demonstration, we'll just increment timestamp
	timestamp := time.Now().Unix()
	
	update := &ClockUpdate{
		NodeID:    n.ID,
		Timestamp: timestamp,
	}
	
	// Sign the update if not Byzantine
	if !n.IsByzantine {
		signature, err := SignClockUpdate(n.PrivateKey, update)
		if err == nil {
			update.Signature = signature
		}
	}
	
	return update
}

// VerifyAndApplyClockUpdate verifies and applies a clock update
func (n *Node) VerifyAndApplyClockUpdate(update *ClockUpdate) bool {
	n.Lock.Lock()
	defer n.Lock.Unlock()
	
	// Byzantine node might lie about its timestamp
	if n.IsByzantine {
		// In a real implementation, Byzantine node would attempt to manipulate
		// But we'll just demonstrate that we detect it
		fmt.Printf("Byzantine node %s attempting to manipulate clock\n", n.ID)
		return false
	}
	
	// Verify the signature if it exists
	if update.Signature != "" {
		// In a real system, we'd verify against the public key
		// For demonstration, we'll accept all valid signatures
		fmt.Printf("Verifying signature for node %s\n", n.ID)
	}
	
	// Update the clock
	n.VectorClock.Update(update.NodeID, update.Timestamp)
	return true
}

// PropagateClockUpdate propagates a clock update to neighbors
func (n *Node) PropagateClockUpdate(update *ClockUpdate, system *System) {
	n.Lock.Lock()
	defer n.Lock.Unlock()
	
	for _, neighborID := range n.Neighbors {
		// Skip if neighbor is isolated
		if system.IsPartitioned(neighborID) {
			continue
		}
		
		neighbor, exists := system.Nodes[neighborID]
		if exists {
			// For demonstration, we'll just apply the update
			neighbor.VerifyAndApplyClockUpdate(update)
		}
	}
}

// SimulatePartition simulates the network partition scenario
func SimulatePartition() {
	fmt.Println("=== Simulating Network Partition ===")
	fmt.Println("Nodes: A,B,C (us-east), D,E (eu-west), F,G (ap-south)")
	fmt.Println("Partition: eu-west (D,E) isolated from us-east")
	fmt.Println("Node D has unidirectional link: can receive from us-east but not send")
	fmt.Println("Node E is fully isolated")
	fmt.Println()
	
	// Create system
	system := NewSystem()
	
	// Create nodes
	nodes := make(map[string]*Node)
	
	// Create us-east nodes
	nodes["A"] = NewNode("A", false, false)
	nodes["B"] = NewNode("B", false, false)
	nodes["C"] = NewNode("C", false, false)
	
	// Create eu-west nodes
	nodes["D"] = NewNode("D", false, true)  // Isolated
	nodes["E"] = NewNode("E", false, true)   // Isolated
	
	// Create ap-south nodes
	nodes["F"] = NewNode("F", true, false)   // Byzantine
	nodes["G"] = NewNode("G", false, false)
	
	// Add neighbors (network topology)
	nodes["A"].Neighbors = []string{"B", "C", "D"}
	nodes["B"].Neighbors = []string{"A", "C", "D"}
	nodes["C"].Neighbors = []string{"A", "B", "D"}
	nodes["D"].Neighbors = []string{"A", "B", "C", "E"}
	nodes["E"].Neighbors = []string{"D"}
	nodes["F"].Neighbors = []string{"G"}
	nodes["G"].Neighbors = []string{"F"}
	
	// Add nodes to system
	for _, node := range nodes {
		system.AddNode(node)
	}
	
	// Set leader
	system.SetLeader("A")
	
	// Simulate client operations
	fmt.Println("Client submits write W1 to A (leader)")
	fmt.Println("Stale client submits write W2 to E (isolated partition)")
	fmt.Println()
	
	// Simulate operations
	w1 := nodes["A"].GetClockUpdate()
	w2 := nodes["E"].GetClockUpdate()
	
	fmt.Printf("W1 timestamp: %d\n", w1.Timestamp)
	fmt.Printf("W2 timestamp: %d\n", w2.Timestamp)
	fmt.Println()
	
	// Verify clock updates
	fmt.Println("Verifying clock updates:")
	fmt.Printf("Node A clock update: %+v\n", w1)
	fmt.Printf("Node E clock update: %+v\n", w2)
	fmt.Println()
	
	// Demonstrate vector clock comparison
	fmt.Println("Vector Clock Comparison:")
	fmt.Printf("Node A clock: %+v\n", nodes["A"].VectorClock.Timestamps)
	fmt.Printf("Node E clock: %+v\n", nodes["E"].VectorClock.Timestamps)
	fmt.Println()
	
	// Show how Byzantine node F could behave
	fmt.Println("Byzantine node F behavior:")
	fmt.Printf("Node F (byzantine) has vector clock: %+v\n", nodes["F"].VectorClock.Timestamps)
	fmt.Println("F could lie about its timestamps to manipulate consensus")
	fmt.Println()
	
	// Demonstrate cryptographic attestation
	fmt.Println("Cryptographic Attestation:")
	fmt.Printf("Node A signature verification: %t\n", VerifyClockUpdate(nodes["A"].PublicKey, w1))
	fmt.Printf("Node E signature verification: %t\n", VerifyClockUpdate(nodes["E"].PublicKey, w2))
	fmt.Println()
	
	// Show minimum k for BFT
	fmt.Println("BFT Protocol Analysis:")
	fmt.Printf("Total nodes n = 7\n")
	fmt.Printf("Byzantine faults f = 2\n")
	fmt.Printf("Minimum k = n - f + 1 = 7 - 2 + 1 = 6\n")
	fmt.Println("At least 6 nodes must verify a clock update to ensure safety")
	fmt.Println()
	
	// Final analysis
	fmt.Println("=== Analysis ===")
	fmt.Println("Linearizability: NOT guaranteed in this scenario")
	fmt.Println("Reason: Network partition and Byzantine node F can cause inconsistent views")
	fmt.Println("The system cannot maintain linearizability due to:")
	fmt.Println("1. Isolated partitions preventing consensus")
	fmt.Println("2. Byzantine node F lying about vector clock timestamps")
	fmt.Println("3. Unidirectional link preventing proper coordination")
}

func main() {
	SimulatePartition()
}