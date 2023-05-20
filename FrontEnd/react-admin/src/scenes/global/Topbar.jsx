import {Box, IconButton, Avatar, useTheme} from "@mui/material";
import {useContext} from "react";
import {ColorModeContext} from "../../theme";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import Header from "../../components/Header";
import SettingsDropDown from "../../components/topbar/SettingsDropDown";
import UserDropDown from "../../components/topbar/UserDropDown";

const Topbar = ({title, subtitle, ticker}) => {
    const theme = useTheme();
    const colorMode = useContext(ColorModeContext);
    let link = "https://financialmodelingprep.com/image-stock/" + ticker + ".png"

    return (
        <Box display="flex" justifyContent="space-between" p={2}>
            <Box display="flex">
                {ticker && (<Avatar src={link} alt="Image"
                                    style={{marginRight: "14px", marginTop: "12px", width: "50px", height: "50px"}}/>)}
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
