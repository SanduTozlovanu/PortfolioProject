import {Box, Typography, Grid, Divider, CircularProgress, useTheme} from "@mui/material";
import LocalAtmIcon from '@mui/icons-material/LocalAtm';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import PeopleIcon from '@mui/icons-material/People';
import EqualizerIcon from '@mui/icons-material/Equalizer';
import TimelineIcon from '@mui/icons-material/Timeline';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import {tokens} from "../../theme";
import {useNavigate, useParams} from 'react-router-dom';
import {useState, useEffect} from "react";
import config from "../../config.json";
import axios from "axios";
import Topbar from "../global/Topbar";
import StatBox from "../../components/StatBox";
import FinancialStats from "../../components/FinancialStats";
import PriceChartComponent from "../../components/PriceChartComponent";
import RevenueBarChart from "../../components/RevenueBarChart";
import PredictionChartComponent from "../../components/PredictionChartComponent";

const StockProfile = () => {
    const [profile, setProfile] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState({});
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();
    const {stock_name} = useParams();
    const getMarketCap = () => {
        const nr = (profile.mktCap / 1000000000).toFixed(1)
        return nr + " Bln"
    }

    useEffect(() => {
        getProfile()
    }, []);

    const getProfile = async () => {
        try {
            const response = await axios.get(`${config.url}/stock/details/${stock_name}`);
            setProfile(response.data)
            setError("")
            setIsLoading(false)
        } catch (error) {
            console.log(error)
            setError("Failed to get statement!")
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
            <Topbar title={profile.companyName} subtitle={profile.sector + ", " + profile.industry}
                    ticker={stock_name} isTicker={true}/>
            <Grid container spacing={1}>
                <Grid item xs={5} md={5}>
                    <Typography variant="h2" style={{textAlign: 'center'}}>Stats</Typography>
                    <Grid container spacing={2} style={{marginTop: '1px'}}>
                        <Grid item xs={6} md={6}>
                            <StatBox
                                title="Price"
                                value={profile.price}
                                icon={
                                    <AttachMoneyIcon
                                        sx={{color: colors.greenAccent[300], fontSize: "35px"}}
                                    />
                                }
                            />
                        </Grid>
                        <Grid item xs={6} md={6}>
                            <StatBox
                                title="Market Cap"
                                value={getMarketCap()}
                                icon={
                                    <LocalAtmIcon
                                        sx={{color: theme.palette.secondary[100], fontSize: "35px"}}
                                    />
                                }
                            />
                        </Grid>
                        <Grid item xs={6} md={6}>
                            <StatBox
                                title="Average Volume"
                                value={profile.volAvg}
                                icon={
                                    <EqualizerIcon
                                        sx={{color: theme.palette.secondary[100], fontSize: "35px"}}
                                    />
                                }
                            />
                        </Grid>
                        <Grid item xs={6} md={6}>
                            <StatBox
                                title="Beta"
                                value={profile.beta}
                                icon={
                                    <TimelineIcon
                                        sx={{color: theme.palette.secondary[100], fontSize: "35px"}}
                                    />
                                }
                            />
                        </Grid>
                        <Grid item xs={6} md={6}>
                            <StatBox
                                title="Employees"
                                value={profile.fullTimeEmployees}
                                icon={
                                    <PeopleIcon
                                        sx={{color: theme.palette.secondary[100], fontSize: "35px"}}
                                    />
                                }
                            />
                        </Grid>
                        <Grid item xs={6} md={6}>
                            <StatBox
                                value={profile.exchange}
                                icon={
                                    <AccountBalanceIcon
                                        sx={{color: theme.palette.secondary[100], fontSize: "35px"}}
                                    />
                                }
                            />
                        </Grid>
                    </Grid>
                </Grid>
                <Box>
                    <Divider orientation="vertical"
                             sx={{height: "100%", my: 'auto', marginLeft: 2, backgroundColor: colors.primary[400]}}/>
                </Box>
                <Grid item xs={6.5} md={6.5}>
                    <Typography variant="h2" style={{textAlign: 'center'}}>Description</Typography>
                    <Box backgroundColor={colors.primary[400]} style={{margin: '10px'}}>
                        <Typography>{profile.description}</Typography>
                    </Box>
                </Grid>
            </Grid>
            <FinancialStats stock_name={stock_name}></FinancialStats>
            <Grid container spacing={1} style={{marginTop: '10px'}}>
                <Grid item xs={6} md={6}>
                    <PriceChartComponent stock_name={stock_name}></PriceChartComponent>
                </Grid>
                <Grid item xs={6} md={6}>
                    <RevenueBarChart stock_name={stock_name}/>
                </Grid>
            </Grid>
            <PredictionChartComponent stock_name={stock_name}></PredictionChartComponent>

        </Box>
    );
};

export default StockProfile;
