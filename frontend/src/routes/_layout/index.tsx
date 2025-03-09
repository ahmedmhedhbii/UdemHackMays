import { Box, Container, Flex ,Text } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

import useAuth from "@/hooks/useAuth"
import ChatBox from "@/components/Chat/chatBox"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  return (
    <>
      <Container maxW="full">
      <Flex>
        {/* Left Column: Welcome Message */}
        <Box pt={12} m={4}>
          <Text fontSize="2xl" truncate maxW="sm">
            Hi, {currentUser?.full_name || currentUser?.email} 👋🏼
          </Text>
          <Text>Welcome back, nice to see you again!</Text>
        </Box>

        {/* Right Column: Chat Box */}
        <Box flex="1" border="1px solid #ccc" m={4} p={4}>
          <ChatBox />
        </Box>
      </Flex>
    </Container>
    </>
  )
}
