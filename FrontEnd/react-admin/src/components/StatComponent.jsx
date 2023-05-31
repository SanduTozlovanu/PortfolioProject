import {Box, Typography, useTheme} from "@mui/material";
import React from "react";
import {tokens} from "../theme";

const StatComponent = ({ stat, value}) => {
    const theme = useTheme();
    tokens(theme.palette.mode);
    return (
        <Box display="flex" justifyContent="space-between">
            <Typography>{stat}</Typography>
            <Typography>{value}</Typography>
        </Box>
    );
};

export default StatComponent;
