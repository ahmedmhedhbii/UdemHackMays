import { Box, Container, Flex, VStack } from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";

import useAuth from "@/hooks/useAuth";
import ChatBox from "@/components/Chat/chatBox";
import AvailableAppointments from "@/components/Mdashboard/AvailableAppointments";
import WeeklyPatients from "@/components/Mdashboard/weeklyPatients";
// Import the new PatientsList
import PatientsList from "@/components/Mdashboard/patientsList";


export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
});

function Dashboard() {
  useAuth();

  return (
    <Container maxW="full" h="100vh">
      <Flex>
        {/* LEFT COLUMN */}
        <VStack
          //spacing={4}
          align="stretch"
          p={4}
          w={{ base: "100%", md: "70%" }}
          bg="gray.50"
        >
          {/* Existing components */}
          <AvailableAppointments />
          <WeeklyPatients />

          {/* New Search Zone */}
          <PatientsList />
        </VStack>

        {/* RIGHT COLUMN: Chat Box */}
        <Box
          w={{ base: "100%", md: "30%" }}
          p={4}
          ml="auto"
          borderLeft="1px solid #ccc"
          bg="white"
        >
          <ChatBox />
        </Box>
      </Flex>
    </Container>
  );
}

export default Dashboard;
