import { useState } from "react";
import {
  Box,
  Text,
  Input,
  Button,
  VStack,
  HStack,
} from "@chakra-ui/react";
import { useNavigate } from "@tanstack/react-router";
// Import the dynamic route from $clientId.tsx
import { Route as patientDetailsRoute } from "@/routes/_layout/client/$clientId";

function PatientsList() {
  // Mock patient data with IDs
  const [patients] = useState([
    { id: "p1", name: "John Doe" },
    { id: "p2", name: "Jane Smith" },
    { id: "p3", name: "Alice Johnson" },
  ]);

  // Search state
  const [searchTerm, setSearchTerm] = useState("");

  // Filter patients based on search term
  const filteredPatients = patients.filter((patient) =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // We'll navigate to the dynamic route on click
  const navigate = useNavigate({ from: "." });

  const handlePatientClick = (patientId: string) => {
    // Navigate to the route defined in $clientId.tsx
    // Pass the clicked patient's ID as "clientId"
    navigate({
      to: patientDetailsRoute,
      params: { clientId: patientId },
    });
  };

  return (
    <Box p={4} bg="white" boxShadow="md" borderRadius="md">
      <Text fontWeight="bold" fontSize="lg" mb={2}>
        Search Patients
      </Text>
      <HStack mb={4}>
        <Input
          placeholder="Enter patient name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          borderColor="gray.300"
          _focus={{ borderColor: "teal.500", boxShadow: "outline" }}
        />
        <Button onClick={() => console.log("Searching...")} colorScheme="teal">
          Search
        </Button>
      </HStack>
      <VStack align="stretch" spacing={2}>
        {filteredPatients.map((patient) => (
          <Box
            key={patient.id}
            p={2}
            borderRadius="md"
            _hover={{ bg: "gray.100", cursor: "pointer" }}
            onClick={() => handlePatientClick(patient.id)}
          >
            {patient.name}
          </Box>
        ))}
      </VStack>
    </Box>
  );
}

export default PatientsList;
