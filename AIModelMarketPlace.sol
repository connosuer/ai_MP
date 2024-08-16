pragma solidity ^0.8.0;

contract AIModelMarketplace {
    struct Model {
        address owner;
        string name;
        string description;
        uint256 price;
        bool isAvailable;
    }

    mapping(uint256 => Model) public models;
    uint256 public modelCount;

    event ModelListed(uint256 indexed modelId, address indexed owner, string name, uint256 price);
    event ModelPurchased(uint256 indexed modelId, address indexed buyer, address indexed seller, uint256 price);

    function listModel(string memory _name, string memory _description, uint256 _price) public {
        modelCount++;
        models[modelCount] = Model(msg.sender, _name, _description, _price, true);
        emit ModelListed(modelCount, msg.sender, _name, _price);
    }

    function purchaseModel(uint256 _modelId) public payable {
        Model storage model = models[_modelId];
        require(model.isAvailable, "Model is not available");
        require(msg.value >= model.price, "Insufficient payment");

        model.isAvailable = false;
        payable(model.owner).transfer(msg.value);

        emit ModelPurchased(_modelId, msg.sender, model.owner, msg.value);
    }
}