import React, {useEffect, useState} from "react";
import {Box, Grid, Typography, useTheme} from "@mui/material";
import {tokens} from "../../theme";
import axios from "axios";
import config from "../../config.json";
import StatComponent from "../StatComponent";

const PortfolioStats = ({ onSetCurrentValue }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [portfolioStats, setPortfolioStats] = useState({});
    const [error, setError] = useState({});

    useEffect(() => {
        getPortfolioStats()
    }, []);
    const getPortfolioStats = async () => {
        try{
            const response = await axios.get(`${config.url}/portfolio/stats`, {
                headers: {
                    Authorization: JSON.parse(localStorage.getItem("user")).token,
                }
            });
            setPortfolioStats(response.data)
            onSetCurrentValue(response.data.currentValue)
            setError("")
        } catch(error){
            console.log(error)
            setError("Failed to get portfolio stats!")
        }
    }
    return (
        <Box>
            <Box style={{margin: '10px'}}>
                <Typography variant="h2" style={{textAlign: 'center'}}>Portfolio Metrics</Typography>
            </Box>
            <Box height="20px"></Box>
            <Grid container spacing={2} sx={{ padding: '10px 10px' }} backgroundColor={colors.blueAccent[800]}>
                <Grid item xs={4} md={4}>
                    <Typography variant="h4" style={{textAlign: 'left', marginBottom:"2px"}}>Value</Typography>
                    <StatComponent stat="Initial value" value={portfolioStats.initialValue}></StatComponent>
                    <StatComponent stat="Current value" value={portfolioStats.currentValue}></StatComponent>
                    <StatComponent stat="Holdings" value={portfolioStats.holdings}></StatComponent>
                </Grid>
                <Grid item xs={4} md={4}>
                    <Typography variant="h4" style={{textAlign: 'left', marginBottom:"2px"}}>Records</Typography>
                    <StatComponent stat="Highest value" value={portfolioStats.highestValue}></StatComponent>
                    <StatComponent stat="Lowest value" value={portfolioStats.lowestValue}></StatComponent>
                    <StatComponent stat="Beta" value={portfolioStats.beta}></StatComponent>
                </Grid>
                <Grid item xs={4} md={4}>
                    <Typography variant="h4" style={{textAlign: 'left', marginBottom:"2px"}}>Benchmark</Typography>
                    <StatComponent stat="Portfolio return" value={portfolioStats.portfolioReturn}></StatComponent>
                    <StatComponent stat="S&P return" value={portfolioStats.snpReturn}></StatComponent>
                    <StatComponent stat="Benchmark delta" value={portfolioStats.benchmarkDelta}></StatComponent>
                </Grid>
            </Grid>
        </Box>
    );
};

export default PortfolioStats;