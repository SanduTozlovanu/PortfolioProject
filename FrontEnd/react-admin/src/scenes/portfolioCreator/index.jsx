import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import BalanceIcon from '@mui/icons-material/Balance';
import ScaleIcon from '@mui/icons-material/Scale';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import InsightsIcon from '@mui/icons-material/Insights';
import {Box, Button, Card, CardContent, Grid, Typography, useTheme} from "@mui/material";
import {tokens} from "../../theme";
import {useNavigate} from 'react-router-dom';
import Topbar from "../global/Topbar";

const PortfolioCreator = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();
    const generateButtonStyle = {
        marginTop: 16,
        color: colors.primary[500],
        fontSize: 20,
        fontWeight: "bold",
        backgroundColor: colors.greenAccent[400]
    };

    return (
        <Box m="20px">
            <Topbar title="PORTFOLIO CREATOR" subtitle="Select a investing strategy for your portfolio"
                    ticker={'portfolioCreator'} isTicker={false}/>
            <Box display="flex" justifyContent="space-between">
                <Card sx={{
                    display: 'flex', backgroundColor: colors.primary[400], transition: 'background-color 0.3s ease',
                    '&:hover': {
                        backgroundColor: colors.primary[500],
                    }
                }}>
                    <Box
                        sx={{display: 'flex', flexDirection: 'column', justifyContent: "center", alignItems: "center"}}>
                        <BalanceIcon sx={{width: "200px", height: "200px"}}/>
                    </Box>
                    <Box sx={{display: 'flex', flexDirection: 'column'}}>
                        <CardContent>
                            <Typography variant="h3">Equal-Weight S&P 500 Index Fund Investing</Typography>
                            <Box sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: "center",
                                alignItems: "center"
                            }}>
                                <Button variant="contained" size="large" style={generateButtonStyle} onClick={() => navigate('/portfolioScreener/equalWeight')}>Generate</Button>
                            </Box>
                        </CardContent>
                        <Box sx={{display: 'flex', alignItems: 'center', justifyContent: "center", pl: 1, pb: 1}}>
                            <Typography variant="h6">This Strategy involves dividing your portfolio balance equally
                                between all S&P 500 stocks, thus resulting a fixed weight
                                that is allocated to each company. This fixed sum is used to buy stocks from each
                                company, according to each company's share price. <span
                                    style={{color: colors.redAccent[300]}}>For an optimal distribution,
                                it is advised to have a budget that is at least 100 000$ worth.</span></Typography>
                        </Box>
                    </Box>
                </Card>
                <Card sx={{
                    display: 'flex',
                    marginLeft: "20px",
                    backgroundColor: colors.primary[500],
                    transition: 'background-color 0.3s ease',
                    '&:hover': {
                        backgroundColor: colors.primary[600],
                    }
                }}>
                    <Box
                        sx={{display: 'flex', flexDirection: 'column', justifyContent: "center", alignItems: "center"}}>
                        <ScaleIcon sx={{width: "200px", height: "200px"}}/>
                    </Box>
                    <Box sx={{display: 'flex', flexDirection: 'column'}}>
                        <CardContent>
                            <Typography variant="h3">Weighted S&P 500 Index Fund Investing</Typography>
                            <Box sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: "center",
                                alignItems: "center"
                            }}>
                                <Button variant="contained" size="large" style={generateButtonStyle} onClick={() => navigate('/portfolioScreener/weighted')}>Generate</Button>
                            </Box>
                        </CardContent>
                        <Box sx={{display: 'flex', alignItems: 'center', justifyContent: "center", pl: 1, pb: 1}}>
                            <Typography variant="h6">This Strategy implies a weighted division of your balance between
                                S&P 500 stocks, resulting in a Market Capitalization weighted distribution.
                                This implies that Giant companies like Apple will have a bigger portion of your
                                portfolio than smaller companies.
                                <span style={{color: colors.redAccent[300]}}>For an optimal distribution,
                                it is advised to have a budget that is at least 100 000$ worth.</span></Typography>
                        </Box>
                    </Box>
                </Card>
            </Box>
            <Box display="flex" justifyContent="space-between" marginTop="20px">
                <Card sx={{
                    display: 'flex', backgroundColor: colors.primary[600], transition: 'background-color 0.3s ease',
                    '&:hover': {
                        backgroundColor: colors.primary[700],
                    }
                }}>
                    <Box
                        sx={{display: 'flex', flexDirection: 'column', justifyContent: "center", alignItems: "center"}}>
                        <TrendingUpIcon sx={{width: "200px", height: "200px"}}/>
                    </Box>
                    <Box sx={{display: 'flex', flexDirection: 'column'}}>
                        <CardContent>
                            <Typography variant="h3">Quantitative Momentum Investing</Typography>
                            <Box sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: "center",
                                alignItems: "center"
                            }}>
                                <Button variant="contained" size="large" style={generateButtonStyle} onClick={() => navigate('/portfolioScreener/momentum')}>Generate</Button>
                            </Box>
                        </CardContent>
                        <Box sx={{display: 'flex', alignItems: 'center', justifyContent: "center", pl: 1, pb: 1}}>
                            <Typography variant="h6">Quantitative momentum investing is a strategy that aims to identify
                                stocks or assets showing strong positive price momentum. It relies on quantitative
                                analysis and mathematical models to select investments that have exhibited upward price
                                trends in the past. The strategy assumes that assets that have performed well recently
                                will continue to perform well in the near future, focusing on capturing the upward
                                momentum.</Typography>
                        </Box>
                    </Box>
                </Card>
                <Card sx={{
                    display: 'flex',
                    marginLeft: "20px",
                    backgroundColor: colors.primary[300],
                    transition: 'background-color 0.3s ease',
                    '&:hover': {
                        backgroundColor: colors.primary[400],
                    }
                }}>
                    <Box
                        sx={{display: 'flex', flexDirection: 'column', justifyContent: "center", alignItems: "center"}}>
                        <AnalyticsIcon sx={{width: "200px", height: "200px"}}/>
                    </Box>
                    <Box sx={{display: 'flex', flexDirection: 'column'}}>
                        <CardContent>
                            <Typography variant="h3">Quantitative Value Investing</Typography>
                            <Box sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: "center",
                                alignItems: "center"
                            }}>
                                <Button variant="contained" size="large" style={generateButtonStyle} onClick={() => navigate('/portfolioScreener/value')}>Generate</Button>
                            </Box>
                        </CardContent>
                        <Box sx={{display: 'flex', alignItems: 'center', justifyContent: "center", pl: 1, pb: 1}}>
                            <Typography variant="h6">
                                Quantitative value investing is a strategy that seeks to identify undervalued stocks or
                                assets based on quantitative analysis and financial metrics. It involves using
                                mathematical models and screening criteria to select investments trading at prices below
                                their intrinsic value. The strategy aims to capitalize on market inefficiencies and
                                potential price appreciation as the market recognizes the true value of the undervalued
                                assets.</Typography>
                        </Box>
                    </Box>
                </Card>
            </Box>
            <Grid container spacing={1} marginTop="20px" paddingBottom="20px">
                <Grid item xs={3} md={3}>
                </Grid>
                <Grid item xs={6} md={6}>
                    <Card sx={{
                        display: 'flex', backgroundColor: colors.primary[400], transition: 'background-color 0.3s ease',
                        '&:hover': {
                            backgroundColor: colors.primary[500],
                        }
                    }}>
                        <Box
                            sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: "center",
                                alignItems: "center"
                            }}>
                            <InsightsIcon sx={{width: "200px", height: "200px"}}/>
                        </Box>
                        <Box sx={{display: 'flex', flexDirection: 'column'}}>
                            <CardContent>
                                <Typography variant="h3">Quantitative Momentum & Value Investing</Typography>
                                <Box sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    justifyContent: "center",
                                    alignItems: "center"
                                }}>
                                    <Button variant="contained" size="large"
                                            style={generateButtonStyle} onClick={() => navigate('/portfolioScreener/valueMomentum')}>Generate</Button>
                                </Box>
                            </CardContent>
                            <Box sx={{display: 'flex', alignItems: 'center', justifyContent: "center", pl: 1, pb: 1}}>
                                <Typography variant="h6">Quantitative value and momentum investing is a strategy that
                                    combines the principles of both value and momentum investing. It aims to identify
                                    undervalued assets that also exhibit positive price momentum. By using quantitative
                                    analysis and mathematical models, the strategy seeks to find investments that have
                                    the potential for both price appreciation and the ability to outperform the market.
                                    It leverages value metrics to identify undervalued assets and momentum indicators to
                                    capture the upward price trends for potential returns.</Typography>
                            </Box>
                        </Box>
                    </Card>

                </Grid>
                <Grid item xs={3} md={3}>
                </Grid>
            </Grid>
        </Box>
    )
        ;
};

export default PortfolioCreator;
