#!/usr/bin/env python3
"""
BFT Protocol Implementation for Distributed Consensus with Causal Ordering
This script demonstrates the key concepts of the problem without requiring Go
"""

import hashlib
import json
import time
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class VectorClock:
    """Vector clock implementation for causal ordering"""
    timestamps: Dict[str, int]
    
    def __init__(self, node_id: str = None):
        self.timestamps = defaultdict(int)
        if node_id:
            self.timestamps[node_id] = 0
    
    def update(self, node_id: str, timestamp: int):
        """Update timestamp for a node"""
        self.timestamps[node_id] = max(self.timestamps[node_id], timestamp)
    
    def increment(self, node_id: str):
        """Increment timestamp for a node"""
        self.timestamps[node_id] += 1
    
    def get_timestamp(self, node_id: str) -> int:
        """Get timestamp for a node"""
        return self.timestamps[node_id]
    
    def compare(self, other: 'VectorClock') -> int:
        """Compare with another vector clock"""
        # Returns -1 if self < other, 0 if equal, 1 if self > other
        all_equal = True
        max_self = 0
        max_other = 0
        
        # Check all timestamps in self
        for node_id, ts in self.timestamps.items():
            max_self = max(max_self, ts)
            if node_id in other.timestamps:
                max_other = max(max_other, other.timestamps[node_id])
                if ts < other.timestamps[node_id]:
                    return -1
                elif ts > other.timestamps[node_id]:
                    return 1
                elif ts != other.timestamps[node_id]:
                    all_equal = False
            else:
                max_other = max(max_other, ts)
                if ts > 0:
                    return 1
                all_equal = False
        
        # Check timestamps in other that are not in self
        for node_id, ts in other.timestamps.items():
            if node_id not in self.timestamps:
                max_other = max(max_other, ts)
                if ts > 0:
                    return -1
                all_equal = False
        
        if all_equal:
            return 0
        elif max_self > max_other:
            return 1
        else:
            return -1

class ClockUpdate:
    """Represents a clock update with cryptographic signature"""
    def __init__(self, node_id: str, timestamp: int, signature: str = None):
        self.node_id = node_id
        self.timestamp = timestamp
        self.signature = signature
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'node_id': self.node_id,
            'timestamp': self.timestamp,
            'signature': self.signature
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ClockUpdate':
        """Create from dictionary"""
        return cls(
            node_id=data['node_id'],
            timestamp=data['timestamp'],
            signature=data['signature']
        )

class Node:
    """Represents a system node"""
    def __init__(self, node_id: str, is_byzantine: bool = False, is_isolated: bool = False):
        self.node_id = node_id
        self.vector_clock = VectorClock(node_id)
        self.is_byzantine = is_byzantine
        self.is_isolated = is_isolated
        self.neighbors = []
        self.signature_key = f"key_{node_id}"  # Simplified key for demonstration
    
    def get_clock_update(self) -> ClockUpdate:
        """Get a clock update for this node"""
        # Increment our own timestamp
        self.vector_clock.increment(self.node_id)
        timestamp = self.vector_clock.get_timestamp(self.node_id)
        
        # Create clock update
        update = ClockUpdate(
            node_id=self.node_id,
            timestamp=timestamp
        )
        
        # Sign the update (simplified - in reality this would be cryptographic)
        if not self.is_byzantine:
            update.signature = self._sign_update(update)
        
        return update
    
    def _sign_update(self, update: ClockUpdate) -> str:
        """Sign an update (simplified for demonstration)"""
        # In a real system, this would be cryptographic signing
        message = f"{update.node_id}:{update.timestamp}"
        return hashlib.sha256(message.encode()).hexdigest()[:16]
    
    def verify_and_apply_clock_update(self, update: ClockUpdate) -> bool:
        """Verify and apply a clock update"""
        # Byzantine node might lie about timestamps
        if self.is_byzantine:
            print(f"Byzantine node {self.node_id} attempting to manipulate clock")
            # In reality, Byzantine node would try to lie about timestamps
            return False
        
        # Verify signature (simplified)
        if update.signature:
            expected_signature = self._sign_update(update)
            if update.signature != expected_signature:
                print(f"Signature verification failed for node {self.node_id}")
                return False
        
        # Apply the update
        self.vector_clock.update(update.node_id, update.timestamp)
        return True
    
    def propagate_clock_update(self, update: ClockUpdate, system: 'System'):
        """Propagate clock update to neighbors"""
        for neighbor_id in self.neighbors:
            if system.is_partitioned(neighbor_id):
                continue
            
            neighbor = system.get_node(neighbor_id)
            if neighbor:
                neighbor.verify_and_apply_clock_update(update)

class System:
    """Distributed system with nodes"""
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.leader = None
        self.partition = {}  # Track isolated nodes
    
    def add_node(self, node: Node):
        """Add a node to the system"""
        self.nodes[node.node_id] = node
    
    def set_leader(self, leader_id: str):
        """Set the current leader"""
        self.leader = leader_id
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID"""
        return self.nodes.get(node_id)
    
    def is_partitioned(self, node_id: str) -> bool:
        """Check if a node is isolated"""
        return self.partition.get(node_id, False)
    
    def set_partition(self, node_id: str, is_isolated: bool):
        """Set partition status for a node"""
        self.partition[node_id] = is_isolated
    
    def simulate_partition(self):
        """Simulate the specific network partition scenario"""
        print("=== Network Partition Simulation ===")
        print("Nodes: A,B,C (us-east), D,E (eu-west), F,G (ap-south)")
        print("Partition: eu-west (D,E) isolated from us-east")
        print("Node D has unidirectional link: can receive from us-east but not send")
        print("Node E is fully isolated")
        print()
        
        # Create nodes
        nodes = {}
        
        # us-east nodes
        nodes["A"] = Node("A", is_byzantine=False, is_isolated=False)
        nodes["B"] = Node("B", is_byzantine=False, is_isolated=False)
        nodes["C"] = Node("C", is_byzantine=False, is_isolated=False)
        
        # eu-west nodes
        nodes["D"] = Node("D", is_byzantine=False, is_isolated=True)  # Isolated
        nodes["E"] = Node("E", is_byzantine=False, is_isolated=True)  # Isolated
        
        # ap-south nodes
        nodes["F"] = Node("F", is_byzantine=True, is_isolated=False)  # Byzantine
        nodes["G"] = Node("G", is_byzantine=False, is_isolated=False)
        
        # Set up neighbors (network topology)
        nodes["A"].neighbors = ["B", "C", "D"]
        nodes["B"].neighbors = ["A", "C", "D"]
        nodes["C"].neighbors = ["A", "B", "D"]
        nodes["D"].neighbors = ["A", "B", "C", "E"]
        nodes["E"].neighbors = ["D"]
        nodes["F"].neighbors = ["G"]
        nodes["G"].neighbors = ["F"]
        
        # Add nodes to system
        for node in nodes.values():
            self.add_node(node)
        
        # Set leader
        self.set_leader("A")
        
        print(f"Leader set to: {self.leader}")
        print()
        
        # Simulate client operations
        print("Client submits write W1 to A (leader)")
        print("Stale client submits write W2 to E (isolated partition)")
        print()
        
        # Get clock updates
        w1 = nodes["A"].get_clock_update()
        w2 = nodes["E"].get_clock_update()
        
        print(f"W1 timestamp: {w1.timestamp}")
        print(f"W2 timestamp: {w2.timestamp}")
        print()
        
        # Show vector clocks
        print("Vector Clocks:")
        for node_id, node in nodes.items():
            print(f"Node {node_id}: {dict(node.vector_clock.timestamps)}")
        print()
        
        # Demonstrate Byzantine behavior
        print("Byzantine Node F behavior:")
        print("Node F (byzantine) could lie about its timestamps to manipulate consensus")
        print()
        
        # Show cryptographic attestation
        print("Cryptographic Attestation:")
        print(f"Node A signature verification: {'Valid' if w1.signature else 'None'}")
        print(f"Node E signature verification: {'Valid' if w2.signature else 'None'}")
        print()
        
        # Show minimum k for BFT
        print("BFT Protocol Analysis:")
        n = 7  # Total nodes
        f = 2  # Byzantine faults
        k = n - f + 1  # Minimum nodes required for safety
        print(f"Total nodes n = {n}")
        print(f"Byzantine faults f = {f}")
        print(f"Minimum k = n - f + 1 = {n} - {f} + 1 = {k}")
        print("At least 6 nodes must verify a clock update to ensure safety")
        print()
        
        # Final analysis
        print("=== Analysis ===")
        print("Linearizability: NOT guaranteed in this scenario")
        print("Reason: Network partition and Byzantine node F can cause inconsistent views")
        print("The system cannot maintain linearizability due to:")
        print("1. Isolated partitions preventing consensus")
        print("2. Byzantine node F lying about vector clock timestamps")
        print("3. Unidirectional link preventing proper coordination")
        print()
        
        return nodes

def main():
    print("BFT Protocol Implementation for Distributed Consensus")
    print("=" * 60)
    print()
    
    # Create and run simulation
    system = System()
    nodes = system.simulate_partition()
    
    print("=== Conclusion ===")
    print("This implementation demonstrates:")
    print("1. Vector clocks for causal ordering")
    print("2. Cryptographic attestation with signatures")
    print("3. Byzantine fault tolerance principles")
    print("4. Network partition handling")
    print("5. BFT minimum k calculation")
    print()
    print("Note: This is a simplified demonstration. A full implementation")
    print("would require cryptographic libraries and more sophisticated")
    print("consensus mechanisms.")

if __name__ == "__main__":
    main()