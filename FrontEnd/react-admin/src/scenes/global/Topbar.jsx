import {Box, IconButton, Avatar, useTheme} from "@mui/material";
import {useContext} from "react";
import {ColorModeContext} from "../../theme";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import NewspaperIcon from '@mui/icons-material/Newspaper';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import WorkIcon from '@mui/icons-material/Work';
import Header from "../../components/Header";
import SettingsDropDown from "../../components/topbar/SettingsDropDown";
import UserDropDown from "../../components/topbar/UserDropDown";

const Topbar = ({title, subtitle, ticker, isTicker}) => {
    const theme = useTheme();
    const colorMode = useContext(ColorModeContext);
    let link = "https://financialmodelingprep.com/image-stock/" + ticker + ".png"
    let isMyPortfolio = (ticker === "myPortfolio");
    let isNews = (ticker === "news");
    let isStockScreener = (ticker === "stockScreener");
    let isTransactionHistory = (ticker === "transactionHistory");

    return (
        <Box display="flex" justifyContent="space-between" p={2}>
            <Box display="flex">
                {ticker && isTicker && (<Avatar src={link} alt="Image"
                                    style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isMyPortfolio && (<WorkIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isStockScreener && (<QueryStatsIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isTransactionHistory && (<ReceiptLongIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                {isNews && (<NewspaperIcon style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
                <Header
                    title={title}
                    subtitle={subtitle}
                />
            </Box>

            {/* ICONS */}
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
                <SettingsDropDown/>
                <UserDropDown/>
            </Box>
        </Box>
    );
};

export default Topbar;
