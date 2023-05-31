import React from "react";
import {useNavigate} from "react-router-dom";
import {Avatar, Box, Typography, useTheme} from "@mui/material";
import SouthIcon from '@mui/icons-material/South';
import NorthIcon from '@mui/icons-material/North';
import {tokens} from "../theme";

const TickerChangeComponent = ({ticker, change}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const color = parseFloat(change) >= 0 ? colors.greenAccent[500] : colors.redAccent[500]
    const style = {height:"60%", marginTop: 3}
    const icon = parseFloat(change) >= 0 ? <NorthIcon style={style}/> : <SouthIcon style={style}/>
    const navigate = useNavigate()
    let link = "https://financialmodelingprep.com/image-stock/" + ticker + ".png"
    return (
        <Box display="flex" justifyContent="space-between" backgroundColor={colors.blueAccent[800]} style={{cursor: "pointer"}}
             borderRadius="0.55rem" p="0.5rem 0.5rem" onClick={() => navigate(`/stockProfile/${ticker}`)}>
            <Box display="flex">
                <Avatar src={link} alt="Image" style={{width: "20px", height: "20px"}}/>
                <Typography variant="h5" style={{marginLeft:5}}>{ticker}</Typography>
            </Box>
            <Box display="flex">
                {icon}
                <Typography variant="h5" color={color}> {change}% </Typography>
            </Box>
        </Box>
    );
};

export default TickerChangeComponent;