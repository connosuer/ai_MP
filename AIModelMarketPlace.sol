pragma solidity ^0.8.0;

contract AIModelMarketplace {
    struct Model {
        string name;
        string description;
        address payable owner;
        uint256 price;
        bool isAvailable;
        string ipfsHash;
        uint256 totalRating;
        uint256 ratingCount;
    }

    struct Composition {
        string name;
        string description;
        address creator;
        uint256[] modelIds;
    }

    mapping(uint256 => Model) public models;
    uint256 public modelCount;

    mapping(uint256 => Composition) public compositions;
    uint256 public compositionCount;

    event ModelListed(uint256 indexed modelId, address indexed owner, string name, uint256 price);
    event ModelPurchased(uint256 indexed modelId, address indexed buyer, address indexed seller, uint256 price);
    event CompositionCreated(uint256 indexed compositionId, address indexed creator, string name);

    // ... (previous functions remain the same)

    function createComposition(string memory _name, string memory _description, uint256[] memory _modelIds) public {
        require(_modelIds.length >= 2, "Composition must include at least two models");
        
        compositionCount++;
        compositions[compositionCount] = Composition(_name, _description, msg.sender, _modelIds);
        
        emit CompositionCreated(compositionCount, msg.sender, _name);
    }

    function getComposition(uint256 _compositionId) public view returns (string memory, string memory, address, uint256[] memory) {
        Composition storage composition = compositions[_compositionId];
        return (composition.name, composition.description, composition.creator, composition.modelIds);
    }

    function getCompositionCount() public view returns (uint256) {
        return compositionCount;
    }

    function getModelCount() public view returns (uint256) {
    return modelCount;
}
}