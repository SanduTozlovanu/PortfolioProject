import React from 'react';
import { IconButton, Menu, MenuItem } from '@mui/material';
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
function SettingsDropDown() {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <div>
            <IconButton
                aria-controls="dropdown-menu"
                aria-haspopup="true"
                onClick={handleClick}
            >
                <SettingsOutlinedIcon />
            </IconButton>
            <Menu
                id="dropdown-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem onClick={handleClose}>Option 1</MenuItem>
                <MenuItem onClick={handleClose}>Option 2</MenuItem>
                <MenuItem onClick={handleClose}>Option 3</MenuItem>
            </Menu>
        </div>
    );
}
export default SettingsDropDown