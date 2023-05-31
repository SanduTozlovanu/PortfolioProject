import React, {useEffect, useState} from "react";
import {Box, Grid, Typography, useTheme} from "@mui/material";
import {tokens} from "../theme";
import axios from "axios";
import config from "../config.json";
import StatComponent from "./StatComponent";

const FinancialStats = ({stock_name}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [finStats, setFinStats] = useState({});
    const [, setError] = useState({});

    useEffect(() => {
        getFinancialStats()
    }, []);
    const getFinancialStats = async () => {
        try{
            const response = await axios.get(`${config.url}/stock/finances/${stock_name}`);
            setFinStats(response.data)
            setError("")
        } catch(error){
            console.log(error)
            setError("Failed to get financial stats!")
        }
    }
    return (
        <Box>
            <Box style={{margin: '10px'}}>
                <Typography variant="h2" style={{textAlign: 'center'}}>Earnings: {finStats.title}</Typography>
            </Box>
            <Box height="20px"></Box>
            <Grid container spacing={2} sx={{ padding: '10px 10px' }} backgroundColor={colors.blueAccent[800]}>
                <Grid item xs={3} md={3}>
                    <Typography variant="h4" style={{textAlign: 'left', marginBottom:"2px"}}> Valuation</Typography>
                    <StatComponent stat="P/E" value={finStats.pe}></StatComponent>
                    <StatComponent stat="Price To Sales" value={finStats.priceToSales}></StatComponent>
                    <StatComponent stat="EV to EBITDA" value={finStats.evToEbitda}></StatComponent>
                    <StatComponent stat="Price to Book" value={finStats.priceToBookRatio}></StatComponent>
                    <StatComponent stat="Free Cash Flow Yield" value={finStats.freeCashFlowYield}></StatComponent>
                </Grid>
                <Grid item xs={3} md={3}>
                    <Typography variant="h4" style={{textAlign: 'left', marginBottom:"2px"}}> Income & Expenses</Typography>
                    <StatComponent stat="Gross Profit" value={finStats.grossProfit}></StatComponent>
                    <StatComponent stat="Net Income" value={finStats.netIncome}></StatComponent>
                    <StatComponent stat="Revenue" value={finStats.revenue}></StatComponent>
                    <StatComponent stat="Operating Expenses" value={finStats.operatingExpenses}></StatComponent>
                    <StatComponent stat="EBT per EBIT" value={finStats.ebtPerEbit}></StatComponent>
                </Grid>
                <Grid item xs={3} md={3}>
                    <Typography variant="h4" style={{textAlign: 'left', marginBottom:"2px"}}> Margins & Quality</Typography>
                    <StatComponent stat="Profit Margin" value={finStats.profitMargin}></StatComponent>
                    <StatComponent stat="Operating Margin" value={finStats.operatingMargin}></StatComponent>
                    <StatComponent stat="Piotroski Score" value={finStats.piotroskiScore}></StatComponent>
                    <StatComponent stat="Altman Z Score" value={finStats.altmanZScore}></StatComponent>
                </Grid>
                <Grid item xs={3} md={3}>
                    <Typography variant="h4" style={{textAlign: 'left', marginBottom:"2px"}}> Balance</Typography>
                    <StatComponent stat="Total Cash" value={finStats.totalCash}></StatComponent>
                    <StatComponent stat="Total Debt" value={finStats.totalDebt}></StatComponent>
                    <StatComponent stat="Net" value={finStats.net}></StatComponent>
                    <StatComponent stat="Total Investments" value={finStats.totalInvestments}></StatComponent>
                </Grid>
            </Grid>
        </Box>
    );
};

export default FinancialStats;