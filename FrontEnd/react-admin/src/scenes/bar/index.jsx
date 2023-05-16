import { Box } from "@mui/material";
import Header from "../../components/Header";
import RevenueBarChart from "../../components/RevenueBarChart";

const Bar = () => {
  return (
    <Box m="20px">
      <Header title="Bar Chart" subtitle="Simple Bar Chart" />
      <Box height="75vh">
        <RevenueBarChart />
      </Box>
    </Box>
  );
};

export default Bar;
