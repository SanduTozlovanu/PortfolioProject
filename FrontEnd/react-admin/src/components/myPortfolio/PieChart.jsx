import { ResponsivePie } from "@nivo/pie";
import { tokens } from "../../theme";
import {Box, CircularProgress, useTheme} from "@mui/material";
import React, {useEffect, useState} from "react";
import axios from "axios";
import config from "../../config.json";

const PieChart = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [chartData, setChartData] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    GetPieChartData()
  }, []);
  const GetPieChartData = async () => {
    try{
      const response = await axios.get(`${config.url}/portfolio/chart/holdings`, {
        headers: {
          Authorization: JSON.parse(localStorage.getItem("user")).token,
        },
      });
      setChartData(response.data)
      setIsLoading(false)
      setError("")
    } catch(error){
      console.log(error)
      setIsLoading(false)
      setError("Failed to get financial stats!")
    }
  }
  if (isLoading) {
    return (
        <Box sx={{ display: 'flex', justifyContent:"center", alignItems:"center", height:"30vh"}}>
          <CircularProgress sx={{color: colors.primary[300]}} />
        </Box>
    );
  }
  return (
    <ResponsivePie
      data={chartData}
      theme={{
        axis: {
          domain: {
            line: {
              stroke: colors.grey[100],
            },
          },
          legend: {
            text: {
              fill: colors.grey[100],
            },
          },
          ticks: {
            line: {
              stroke: colors.grey[100],
              strokeWidth: 1,
            },
            text: {
              fill: colors.grey[100],
            },
          },
        },
        tooltip: {
          container: {
            color: colors.grey[900],
          },
        },
      }}
      margin={{ top: 20, right: 80, bottom: 80, left: 20 }}
      innerRadius={0.5}
      padAngle={0.7}
      cornerRadius={3}
      activeOuterRadiusOffset={8}
      borderColor={{
        from: "color",
        modifiers: [["darker", 0.2]],
      }}
      arcLinkLabelsSkipAngle={10}
      arcLinkLabelsTextColor={colors.grey[100]}
      arcLinkLabelsThickness={2}
      arcLinkLabelsColor={{ from: "color" }}
      enableArcLabels={false}
      arcLabelsRadiusOffset={0.4}
      arcLabelsSkipAngle={7}
      arcLabelsTextColor={{
        from: "color",
        modifiers: [["darker", 2]],
      }}
    />
  );
};

export default PieChart;
