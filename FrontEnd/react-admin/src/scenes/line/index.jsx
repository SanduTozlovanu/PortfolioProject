import { Box } from "@mui/material";
import Topbar from "../global/Topbar";
import PortfolioPerformanceChart from "../../components/myPortfolio/PortfolioPerformanceChart";
import React, {useEffect, useState} from "react";
import axios from "axios";
import config from "../../config.json";

const Line = () => {
    const [chartJson, setChartJson] = useState({});
    useEffect(() => {
        getPortfolioStats();
    }, []);
    const getPortfolioStats = async () => {
        try{
            const response = await axios.get(`${config.url}/portfolio/stats`, {
                headers: {
                    Authorization: JSON.parse(localStorage.getItem("user")).token,
                }
            });
            setChartJson(JSON.parse(response.data.chartData))
        } catch(error){
            console.log(error)
        }
    }
  return (
      <Box m="20px">
          <Topbar title="Performance Chart" subtitle="Portfolio Performance Line Chart"
                  ticker={'PerformanceChart'} isTicker={false}/>
          <PortfolioPerformanceChart chartJson={chartJson}/>
      </Box>
  );
};

export default Line;
