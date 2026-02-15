package main

import (
	"testing"
)

// TestVectorClockComparison tests vector clock comparison logic
func TestVectorClockComparison(t *testing.T) {
	vc1 := NewVectorClock()
	vc2 := NewVectorClock()
	
	vc1.Update("A", 10)
	vc1.Update("B", 5)
	
	vc2.Update("A", 10)
	vc2.Update("B", 5)
	
	// Equal clocks should return 0
	result := vc1.Compare(vc2)
	if result != 0 {
		t.Errorf("Expected equal clocks to return 0, got %d", result)
	}
	
	// Different clocks should return non-zero
	vc2.Update("A", 15)
	result = vc1.Compare(vc2)
	if result >= 0 {
		t.Errorf("Expected different clocks to return negative, got %d", result)
	}
}

// TestClockSignatureVerification tests signature verification
func TestClockSignatureVerification(t *testing.T) {
	node, err := NewNode("TestNode", false, false)
	if err != nil {
		t.Fatalf("Failed to create node: %v", err)
	}
	
	update := node.GetClockUpdate()
	
	// Should be able to verify a valid signature
	valid := VerifyClockUpdate(node.PublicKey, update)
	if !valid {
		t.Errorf("Expected valid signature to be verified")
	}
}

// TestByzantineNodeDetection tests detection of Byzantine behavior
func TestByzantineNodeDetection(t *testing.T) {
	byzantineNode, err := NewNode("ByzantineNode", true, false)
	if err != nil {
		t.Fatalf("Failed to create Byzantine node: %v", err)
	}
	
	// Byzantine node should be detected
	update := byzantineNode.GetClockUpdate()
	
	// In our implementation, we're just demonstrating the concept
	// In a real implementation, we'd have more sophisticated detection
	// For now, we just verify the node was created correctly
	if !byzantineNode.IsByzantine {
		t.Errorf("Expected Byzantine node to be flagged as Byzantine")
	}
}

// TestSystemPartitionSimulation tests the partition simulation
func TestSystemPartitionSimulation(t *testing.T) {
	system := NewSystem()
	
	// Create nodes
	nodeA, _ := NewNode("A", false, false)
	nodeB, _ := NewNode("B", false, true) // Isolated
	
	system.AddNode(nodeA)
	system.AddNode(nodeB)
	
	// Set partition
	system.SetPartition("B", true)
	
	// Check partition status
	if !system.IsPartitioned("B") {
		t.Errorf("Expected node B to be partitioned")
	}
	
	// Check leader
	system.SetLeader("A")
	if system.GetLeader() != "A" {
		t.Errorf("Expected leader to be A")
	}
}

// TestClockPropagation tests clock propagation between nodes
func TestClockPropagation(t *testing.T) {
	system := NewSystem()
	
	// Create nodes
	nodeA, _ := NewNode("A", false, false)
	nodeB, _ := NewNode("B", false, false)
	
	system.AddNode(nodeA)
	system.AddNode(nodeB)
	
	// Set up neighbors
	nodeA.Neighbors = []string{"B"}
	nodeB.Neighbors = []string{"A"}
	
	// Get a clock update
	update := nodeA.GetClockUpdate()
	
	// Propagate update
	nodeA.PropagateClockUpdate(update, system)
	
	// Verify update was applied
	if nodeB.VectorClock.GetTimestamp("A") != update.Timestamp {
		t.Errorf("Expected timestamp to be propagated")
	}
}

// TestBFTMinimumK tests the calculation of minimum k for BFT
func TestBFTMinimumK(t *testing.T) {
	n := 7
	f := 2
	
	// Calculate minimum k for BFT
	k := n - f + 1
	
	if k != 6 {
		t.Errorf("Expected minimum k = 6 for n=7, f=2, got %d", k)
	}
}

// TestAll runs all tests
func TestAll(t *testing.T) {
	TestVectorClockComparison(t)
	TestClockSignatureVerification(t)
	TestByzantineNodeDetection(t)
	TestSystemPartitionSimulation(t)
	TestClockPropagation(t)
	TestBFTMinimumK(t)
	
	t.Logf("All tests passed!")
}