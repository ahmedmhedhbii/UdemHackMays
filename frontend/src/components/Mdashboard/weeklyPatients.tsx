import { Box, Text } from "@chakra-ui/react";
// 1) We'll use the router to navigate on click
import { useNavigate } from "@tanstack/react-router";
// 2) Import your client details route (example)
import { Route as clientDetailsRoute } from "@/routes/_layout/client/$clientId"; 
// ^ Adjust the import path if needed

function WeeklyPatients() {
  // Mock data with IDs
  const patients = [
    { id: "c1", name: "John Doe" },
    { id: "c2", name: "Jane Smith" },
    { id: "c3", name: "Bob Johnson" },
  ];

  // Router navigation hook
  const navigate = useNavigate({ from: "." });

  // Click handler
  const handlePatientClick = (patientId: string) => {
    // Navigate to clientDetailsRoute, passing the ID
    navigate({
      to: clientDetailsRoute,
      params: { clientId: patientId },
    });
  };

  return (
    <Box p={4} bg="white" boxShadow="md" borderRadius="md">
      <Text fontWeight="bold" fontSize="lg" mb={2}>
        This Week’s Patients
      </Text>
      {/* Render an unordered list using Box with "as" prop */}
      <Box as="ul" ml={4}>
        {patients.map((patient) => (
          <Box
            as="li"
            key={patient.id}
            mb={2}
            listStyleType="disc"
            fontSize="md"
            // Make the name clickable
            _hover={{ textDecoration: "underline", cursor: "pointer" }}
            onClick={() => handlePatientClick(patient.id)}
          >
            {patient.name}
          </Box>
        ))}
      </Box>
    </Box>
  );
}

export default WeeklyPatients;
