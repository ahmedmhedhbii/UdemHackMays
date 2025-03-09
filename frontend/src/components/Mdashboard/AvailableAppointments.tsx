// src/components/Dashboard/AvailableAppointments.tsx

import { Box, Text } from "@chakra-ui/react";

function AvailableAppointments() {
  const appointments = [
    { date: "12 Jan 2023", time: "9:30 AM" },
    { date: "12 Jan 2023", time: "10:00 AM" },
    { date: "13 Jan 2023", time: "1:00 PM" },
  ];
  
  return (
    <Box p={4} bg="white" boxShadow="md" borderRadius="md">
      <Text fontWeight="bold" fontSize="lg" mb={2}>
        Next Available Appointments
      </Text>
      {appointments.map((appt, idx) => (
        <Text key={idx} mb={1}>
          Appointment {idx + 1}: {appt.date} at {appt.time}
        </Text>
      ))}
    </Box>
  );
}

export default AvailableAppointments;
