import {Box, IconButton, Avatar, useTheme} from "@mui/material";
import {useContext} from "react";
import {ColorModeContext} from "../../theme";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import NewspaperIcon from '@mui/icons-material/Newspaper';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import WorkIcon from '@mui/icons-material/Work';
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import BalanceIcon from '@mui/icons-material/Balance';
import ScaleIcon from '@mui/icons-material/Scale';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import InsightsIcon from '@mui/icons-material/Insights';
import Header from "../../components/Header";
import SettingsDropDown from "../../components/topbar/SettingsDropDown";
import UserDropDown from "../../components/topbar/UserDropDown";
import Authcontext from "../../components/AuthContext";

const Topbar = ({title, subtitle, ticker, isTicker}) => {
    const theme = useTheme();
    const colorMode = useContext(ColorModeContext);
    const {isAuthenticated, setIsAuthenticated, name, setName} = useContext(Authcontext);
    let link = "https://financialmodelingprep.com/image-stock/" + ticker + ".png"
    let isMyPortfolio = (ticker === "myPortfolio");
    let isNews = (ticker === "news");
    let isStockScreener = (ticker === "stockScreener");
    let isTransactionHistory = (ticker === "transactionHistory");
    let isPortfolioCreator = (ticker === "portfolioCreator");
    let isEqualWeight = (ticker === "equalWeight");
    let isWeighted = (ticker === "weighted");
    let isMomentum = (ticker === "momentum");
    let isValue = (ticker === "value");
    let isValueMomentum = (ticker === "valueMomentum");

    return (
        <Box display="flex" justifyContent="space-between" p={2}>
            <Box display="flex">
                {ticker && isTicker && (<Avatar src={link} alt="Image"
                                    style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isMyPortfolio && (<WorkIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isStockScreener && (<QueryStatsIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isTransactionHistory && (<ReceiptLongIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isNews && (<NewspaperIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isPortfolioCreator && (<PrecisionManufacturingIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isEqualWeight && (<BalanceIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isWeighted && (<ScaleIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isMomentum && (<TrendingUpIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isValue && (<AnalyticsIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isValueMomentum && (<InsightsIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                <Header
                    title={title}
                    subtitle={subtitle}
                />
            </Box>

            <Box display="flex">
                <Box>
                    <IconButton onClick={colorMode.toggleColorMode}>
                        {theme.palette.mode === "dark" ? (
                            <DarkModeOutlinedIcon/>
                        ) : (
                            <LightModeOutlinedIcon/>
                        )}
                    </IconButton>
                </Box>
                {isAuthenticated &&<SettingsDropDown/>}
                {isAuthenticated &&<UserDropDown/>}
            </Box>
        </Box>
    );
};

export default Topbar;
