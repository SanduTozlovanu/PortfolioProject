import {Box, Typography, Grid, useTheme, Divider, Button, Pagination} from "@mui/material";
import LocalAtmIcon from '@mui/icons-material/LocalAtm';
import {tokens} from "../../theme";
import React, {useState, useEffect} from "react";
import config from "../../config.json";
import axios from "axios";
import Topbar from "../global/Topbar";
import StatBox from "../../components/StatBox";
import PieChart from "../../components/myPortfolio/PieChart";
import BuyStockForm from "../../components/myPortfolio/BuyStockForm";
import SellStockForm from "../../components/myPortfolio/SellStockForm";
import TickerChangeComponent from "../../components/TickerChangeComponent";
import PortfolioPerformanceChart from "../../components/myPortfolio/PortfolioPerformanceChart";
import PortfolioStats from "../../components/myPortfolio/PortfolioStats";

const MyPortfolio = () => {
    const [gainers, setGainers] = useState([]);
    const [losers, setLosers] = useState([]);
    const [personalised, setPersonalised] = useState([]);
    const [holdingsPerformance, setHoldingsPerformance] = useState([]);
    const [stockBuyOpen, setStockBuyOpen] = useState(false);
    const [stockSellOpen, setStockSellOpen] = useState(false);
    const [currentValue, setCurrentValue] = useState('');
    const [portfolioStats, setPortfolioStats] = useState({});
    const [chartJson, setChartJson] = useState({});
    const componentsPerPage = 9
    const [totalComponents, setTotalComponents] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const startIndex = (currentPage - 1) * componentsPerPage;
    const endIndex = startIndex + componentsPerPage;
    const visibleHoldingPerfomance = holdingsPerformance.slice(startIndex, endIndex);

    const handlePageChange = (event, page) => {
        setCurrentPage(page);
    };

    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const buyStockBtnStyle = {
        marginTop: 16,
        color: colors.primary[500],
        width: "100%",
        fontSize: 19,
        fontWeight: "bold",
        backgroundColor: colors.greenAccent[400],
        ":hover": {backgroundColor: colors.greenAccent[700]}
    };

    const sellStockBtnStyle = {
        marginTop: 16,
        width: "100%",
        color: colors.primary[500],
        fontSize: 19,
        fontWeight: "bold",
        backgroundColor: colors.redAccent[400],
        ":hover": {backgroundColor: colors.redAccent[700]}
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
        getPersonalised();
        getHoldingsPerformance();
        getPortfolioStats();
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

    const getPersonalised = async () => {
        try {
            const response = await axios.get(`${config.url}/stock/personalised`, {
                headers: {
                    Authorization: JSON.parse(localStorage.getItem("user")).token,
                },
            });
            setPersonalised(response.data)
            setError("")
            setIsLoading(false)
        } catch (error) {
            console.log(error)
            setError("Failed to get personalised!")
            setIsLoading(false)
        }
    }

    const getPortfolioStats = async () => {
        try{
            const response = await axios.get(`${config.url}/portfolio/stats`, {
                headers: {
                    Authorization: JSON.parse(localStorage.getItem("user")).token,
                }
            });
            setPortfolioStats(response.data)
            setCurrentValue(response.data.currentValue)
            setChartJson(JSON.parse(response.data.chartData))
            setError("")
        } catch(error){
            console.log(error)
            setError("Failed to get portfolio stats!")
        }
    }
    const getHoldingsPerformance = async () => {
        try {
            const response = await axios.get(`${config.url}/portfolio/stock/performance`, {
                headers: {
                    Authorization: JSON.parse(localStorage.getItem("user")).token,
                },
            });
            setHoldingsPerformance(response.data)
            setTotalComponents(response.data.length)
            setError("")
            setIsLoading(false)
        } catch (error) {
            console.log(error)
            setError("Failed to get my holdings!")
            setIsLoading(false)
        }
    }

    return (
        <Box m="20px">
            <Topbar title="My Portfolio" subtitle="Portfolio Performance Analysis" ticker="myPortfolio" isTicker={false}/>
            <Grid container spacing={1}>
                <Grid item xs={7} md={7}>
                    <Typography variant="h3" style={{textAlign: 'center'}}>Current Holdings</Typography>
                    <Grid container spacing={0} style={{marginTop: '10px'}}>
                        <Grid item xs={9} md={9}>
                            <Box height={370}>
                                <PieChart/>
                            </Box>
                        </Grid>
                        <Grid item xs={3.5} md={3.5} style={{marginTop: 50, marginLeft: -50}}>
                            <StatBox
                                title="Total Value"
                                value={currentValue}
                                icon={
                                    <LocalAtmIcon
                                        sx={{color: theme.palette.secondary[100], fontSize: "35px"}}
                                    />
                                }
                            />
                            <Button variant="contained" size="large" style={buyStockBtnStyle} onClick={handleBuyOpen}>
                                Buy Stocks
                            </Button>
                            <BuyStockForm open={stockBuyOpen} onClose={handleBuyClose}/>
                            <Button variant="contained" size="large" style={sellStockBtnStyle} onClick={handleSellOpen}>
                                Sell Stocks
                            </Button>
                            <SellStockForm open={stockSellOpen} onClose={handleSellClose}/>
                        </Grid>
                    </Grid>
                    <PortfolioStats portfolioStats={portfolioStats}/>
                    <PortfolioPerformanceChart chartJson={chartJson}/>
                    {holdingsPerformance.length !== 0 &&
                        (<Box>
                            <Typography variant="h3" style={{textAlign: 'center', marginTop: 0, marginBottom: 10}}>My
                                Holdings performance</Typography>
                            <Grid container spacing={2} style={{paddingBottom: 30}}>
                                {visibleHoldingPerfomance.map((item) => (
                                    <Grid item xs={4} md={4} key={item.ticker}>
                                        <TickerChangeComponent ticker={item.ticker} change={item.change}/>
                                    </Grid>
                                ))}
                            </Grid>
                            {holdingsPerformance.length > 9 &&(<Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
                                    <Pagination
                                        count={Math.ceil(totalComponents / componentsPerPage)}
                                        page={currentPage}
                                        onChange={handlePageChange}
                                    />
                                </Box>)}
                        </Box>
                        )}
                </Grid>
                <Box>
                    <Divider orientation="vertical"
                             sx={{height: "100%", my: 'auto', marginLeft: 2, backgroundColor: colors.primary[400]}}/>
                </Box>
                <Grid item xs={4.8} md={4.8}>
                    <Typography variant="h3" style={{textAlign: 'center', marginBottom: 10}}>Top gainers
                        today</Typography>
                    <Grid container spacing={2}>
                        {gainers.map((item) => (
                            <Grid item xs={6} md={6} key={item.ticker}>
                                <TickerChangeComponent ticker={item.ticker} change={item.change}/>
                            </Grid>
                        ))}
                    </Grid>
                    <Typography variant="h3" style={{textAlign: 'center', marginBottom: 10, marginTop: 10}}>Top losers
                        today</Typography>
                    <Grid container spacing={2}>
                        {losers.map((item) => (
                            <Grid item xs={6} md={6} key={item.ticker}>
                                <TickerChangeComponent ticker={item.ticker} change={item.change}/>
                            </Grid>
                        ))}
                    </Grid>
                    {personalised.length !== 0 && (
                        <Box><Typography variant="h3" style={{textAlign: 'center', marginBottom: 10, marginTop: 10}}>
                            Stocks for you</Typography>
                            <Grid container spacing={2}>
                                {personalised.map((item) => (
                                    <Grid item xs={6} md={6} key={item.ticker}>
                                        <TickerChangeComponent ticker={item.ticker} change={item.change}/>
                                    </Grid>
                                ))}
                            </Grid>
                        </Box>)}
                </Grid>
            </Grid>
        </Box>
    );
};

export default MyPortfolio;
