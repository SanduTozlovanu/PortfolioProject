import {Box, Typography, Grid, Stack, CircularProgress, useTheme, Divider, Button} from "@mui/material";
import LocalAtmIcon from '@mui/icons-material/LocalAtm';
import {tokens} from "../../theme";
import React, {useState, useEffect} from "react";
import config from "../../config.json";
import axios from "axios";
import Topbar from "../global/Topbar";
import StatBox from "../../components/StatBox";
import PieChart from "../../components/PieChart";
import BuyStockForm from "../../components/myPortfolio/BuyStockForm";
import SellStockForm from "../../components/myPortfolio/SellStockForm";
import TickerChangeComponent from "../../components/myPortfolio/TickerChangeComponent";

const MyPortfolio = () => {
    const [gainers, setGainers] = useState([]);
    const [losers, setLosers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [stockBuyOpen, setStockBuyOpen] = useState(false);
    const [stockSellOpen, setStockSellOpen] = useState(false);
    const [error, setError] = useState({});

    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const buyStockBtnStyle = {
        marginTop: 16,
        color: colors.primary[500],
        width: "100%",
        fontSize: 19,
        fontWeight: "bold",
        backgroundColor: colors.greenAccent[400]
    };

    const sellStockBtnStyle = {
        marginTop: 16,
        width: "100%",
        color: colors.primary[500],
        fontSize: 19,
        fontWeight: "bold",
        backgroundColor: colors.redAccent[400]
    };

    const handleSellOpen = () => {
        setStockSellOpen(true);
    };

    const handleSellClose = () => {
        setStockSellOpen(false);
    };

    const handleBuyOpen = () => {
        setStockBuyOpen(true);
    };

    const handleBuyClose = () => {
        setStockBuyOpen(false);
    };

    useEffect(() => {
        getGainers();
        getLosers();
    }, []);


    const getGainers = async () => {
        try {
            const response = await axios.get(`${config.url}/stock/gainers`);
            setGainers(response.data)
            setError("")
            setIsLoading(false)
        } catch (error) {
            console.log(error)
            setError("Failed to get gainers!")
            setIsLoading(false)
        }
    }

    const getLosers = async () => {
        try {
            const response = await axios.get(`${config.url}/stock/losers`);
            setLosers(response.data)
            setError("")
            setIsLoading(false)
        } catch (error) {
            console.log(error)
            setError("Failed to get losers!")
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return (
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <CircularProgress status="loading"/>
            </div>
        );
    }
    return (
        <Box m="20px">
            <Topbar title="My Portfolio" subtitle="Portfolio Performance Analysis" ticker="myPortfolio"/>
            <Grid container spacing={1}>
                <Grid item xs={7} md={7}>
                    <Grid container spacing={0} style={{marginTop: '1px'}}>
                        <Grid item xs={9} md={9}>
                            <Typography variant="h3" style={{textAlign: 'center'}}>Current Holdings</Typography>
                            <Box height={370}>
                                <PieChart/>
                            </Box>
                        </Grid>
                        <Grid item xs={3.5} md={3.5} style={{marginTop: 70, marginLeft: -50}}>
                            <StatBox
                                title="Total Value"
                                value={"13644$"}
                                icon={
                                    <LocalAtmIcon
                                        sx={{color: theme.palette.secondary[100], fontSize: "35px"}}
                                    />
                                }
                            />
                            <Button variant="contained" size="large" style={buyStockBtnStyle} onClick={handleBuyOpen}>
                                Buy Stocks
                            </Button>
                            <BuyStockForm open={stockBuyOpen} onClose={handleBuyClose} />
                            <Button variant="contained" size="large" style={sellStockBtnStyle} onClick={handleSellOpen}>
                                Sell Stocks
                            </Button>
                            <SellStockForm open={stockSellOpen} onClose={handleSellClose} />
                        </Grid>
                    </Grid>
                </Grid>
                <Box>
                    <Divider orientation="vertical" sx={{height: "100%", my: 'auto', marginLeft: 2, backgroundColor: colors.primary[400]}}/>
                </Box>
                <Grid item xs={4.8} md={4.8}>
                    <Typography variant="h3" style={{textAlign: 'center', marginBottom: 10}}>Top gainers today</Typography>
                    <Grid container spacing={2}>
                        {gainers.map((item, index) => (
                            <Grid item xs={6} md={6}>
                                <TickerChangeComponent ticker={item.ticker} change={item.change}/>
                            </Grid>
                        ))}
                    </Grid>
                    <Typography variant="h3" style={{textAlign: 'center', marginBottom: 10, marginTop: 10}}>Top losers today</Typography>
                    <Grid container spacing={2}>
                        {losers.map((item, index) => (
                            <Grid item xs={6} md={6}>
                                <TickerChangeComponent ticker={item.ticker} change={item.change}/>
                            </Grid>
                        ))}
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    );
};

export default MyPortfolio;
