// routes/_layout/client/clientId.tsx

import { createFileRoute } from "@tanstack/react-router";
import { Box, Heading, Text, VStack, HStack } from "@chakra-ui/react";

// 1) Define the route  
export const Route = createFileRoute("/_layout/client/$clientId")({
  component: ClientDetails,
  parseParams: (params) => ({
    // 2) Tells TypeScript we have a string param named clientId
    clientId: String(params.clientId),
  }),
});

function ClientDetails() {
  // 3) Access the dynamic param
  const { clientId } = Route.useParams();

  // 4) Mock data keyed by clientId
  const mockClientData: Record<string, {
    firstName: string;
    lastName: string;
    dob: string;
    address: string;
    phone: string;
    email: string;
    medicalHistory: string;
    pastConsultations: string[];
    currentMedications: string[];
    notes: string;
  }> = {
    c1: {
      firstName: "John",
      lastName: "Doe",
      dob: "01 Jan 1980",
      address: "123 Main St, Anytown, USA",
      phone: "123-456-7890",
      email: "john@example.com",
      medicalHistory: "Hypertension, Diabetes",
      pastConsultations: [
        "10 Dec 2022: Routine Checkup",
        "05 Nov 2022: Blood Work",
      ],
      currentMedications: ["Metformin", "Lisinopril"],
      notes: "Patient is stable and responding well to treatment.",
    },
    c2: {
      firstName: "Jane",
      lastName: "Smith",
      dob: "02 Feb 1985",
      address: "456 Oak Ave, Othertown, USA",
      phone: "987-654-3210",
      email: "jane@example.com",
      medicalHistory: "Asthma",
      pastConsultations: ["15 Dec 2022: Asthma Follow-up"],
      currentMedications: ["Albuterol"],
      notes: "Needs to schedule a lung function test next quarter.",
    },
    // Add more client IDs as needed...
  };

  // 5) Grab the data for this clientId, or show "Unknown"
  const client = mockClientData[clientId] || {
    firstName: "Unknown",
    lastName: "",
    dob: "N/A",
    address: "N/A",
    phone: "N/A",
    email: "N/A",
    medicalHistory: "N/A",
    pastConsultations: [],
    currentMedications: [],
    notes: "No details available.",
  };

  return (
    <Box p={6} maxW="800px" mx="auto">
      <Heading mb={4} textAlign="center">
        Client Details
      </Heading>
      <VStack align="start" gap={4}>
        <HStack>
          <Text fontWeight="bold">Full Name:</Text>
          <Text>
            {client.firstName} {client.lastName}
          </Text>
        </HStack>
        <HStack>
          <Text fontWeight="bold">Date of Birth:</Text>
          <Text>{client.dob}</Text>
        </HStack>
        <HStack>
          <Text fontWeight="bold">Address:</Text>
          <Text>{client.address}</Text>
        </HStack>
        <HStack>
          <Text fontWeight="bold">Phone:</Text>
          <Text>{client.phone}</Text>
        </HStack>
        <HStack>
          <Text fontWeight="bold">Email:</Text>
          <Text>{client.email}</Text>
        </HStack>
        <Box>
          <Text fontWeight="bold" mb={2}>
            Medical History:
          </Text>
          <Text>{client.medicalHistory}</Text>
        </Box>
        <Box h="1px" bg="gray.200" width="100%" my={4} />
        <Box>
          <Text fontWeight="bold" mb={2}>
            Past Consultations:
          </Text>
          {client.pastConsultations.length > 0 ? (
            <VStack align="start" gap={1}>
              {client.pastConsultations.map((consultation, idx) => (
                <Text key={idx}>• {consultation}</Text>
              ))}
            </VStack>
          ) : (
            <Text>No past consultations available.</Text>
          )}
        </Box>
        <Box>
          <Text fontWeight="bold" mb={2}>
            Current Medications:
          </Text>
          {client.currentMedications.length > 0 ? (
            <VStack align="start" gap={1}>
              {client.currentMedications.map((med, idx) => (
                <Text key={idx}>• {med}</Text>
              ))}
            </VStack>
          ) : (
            <Text>No current medications.</Text>
          )}
        </Box>
        <Box>
          <Text fontWeight="bold" mb={2}>
            Additional Notes:
          </Text>
          <Text>{client.notes}</Text>
        </Box>
      </VStack>
    </Box>
  );
}

export default ClientDetails;
