import React, {useContext} from 'react';
import { IconButton, Menu, MenuItem } from '@mui/material';
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import {useNavigate} from "react-router-dom"
import Authcontext from "../AuthContext";
function UserDropDown() {
    const {setIsAuthenticated, setName } = useContext(Authcontext);
    const [anchorEl, setAnchorEl] = React.useState(null);

    let navigate = useNavigate();

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };
    const logout = () => {
        localStorage.removeItem("user")
        setIsAuthenticated(false)
        setName("")
        navigate("/login")
    }

    return (
        <div>
            <IconButton
                aria-controls="dropdown-menu"
                aria-haspopup="true"
                onClick={handleClick}
            >
                <PersonOutlinedIcon />
            </IconButton>
            <Menu
                id="dropdown-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem onClick={logout}>Logout</MenuItem>
            </Menu>
        </div>
    );
}
export default UserDropDown