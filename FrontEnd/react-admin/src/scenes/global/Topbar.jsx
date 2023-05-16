import {Box, IconButton, Typography, Avatar, useTheme} from "@mui/material";
import { useContext } from "react";
import { ColorModeContext, tokens } from "../../theme";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import Header from "../../components/Header";

const Topbar = ({title, subtitle, ticker}) => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  let link = "https://financialmodelingprep.com/image-stock/" + ticker + ".png"

  return (
    <Box display="flex" justifyContent="space-between" p={2}>
      <Box display="flex">
        {ticker && (<Avatar src={link} alt="Image" style={{marginRight:"14px", marginTop:"12px", width: "50px", height: "50px"}} />)}
        <Header
            title={title}
            subtitle={subtitle}
        />
      </Box>

      {/* ICONS */}
      <Box display="flex">
        <IconButton onClick={colorMode.toggleColorMode}>
          {theme.palette.mode === "dark" ? (
            <DarkModeOutlinedIcon />
          ) : (
            <LightModeOutlinedIcon />
          )}
        </IconButton>
        <IconButton>
          <NotificationsOutlinedIcon />
        </IconButton>
        <IconButton>
          <SettingsOutlinedIcon />
        </IconButton>
        <IconButton>
          <PersonOutlinedIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default Topbar;
